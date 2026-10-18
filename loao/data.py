"""Load, cap, harmonize, de-duplicate and partition one dataset."""

from __future__ import annotations

import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .taxonomy import Taxonomy, normalize_label

META_COLUMNS = ["row_id", "label_raw", "label_norm", "family", "subfamily", "part", "_t_start"]
PARTS = ("train", "val", "test")


def feature_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c not in META_COLUMNS]


def _resolve_files(patterns: list[str], root: Path) -> list[Path]:
    files: list[Path] = []
    for pat in patterns:
        files.extend(Path(p) for p in sorted(glob.glob(str(root / pat))))
    if not files:
        raise FileNotFoundError(f"No files match {patterns} under {root}")
    return files


def _read(path: Path, **kw) -> pd.DataFrame | pd.io.parsers.TextFileReader:
    if path.suffix == ".parquet":
        if "chunksize" in kw:
            kw.pop("chunksize")
            return [pd.read_parquet(path, columns=kw.get("usecols"))]
        return pd.read_parquet(path, columns=kw.get("usecols"))
    return pd.read_csv(path, low_memory=False, **kw)


def count_labels(files: list[Path], label_col: str) -> pd.Series:
    total = pd.Series(dtype="int64")
    for f in files:
        for chunk in _read(f, usecols=[label_col], chunksize=1_000_000):
            vc = chunk[label_col].map(normalize_label).value_counts()
            total = total.add(vc, fill_value=0)
    return total.astype("int64")


def load_capped(cfg: dict, root: Path, max_per_label: int, seed: int) -> tuple[pd.DataFrame, dict]:
    """Two-pass load: count labels, then sample at most `max_per_label` rows per raw label.

    Sampling is deterministic for a given seed and file list.
    """
    files = _resolve_files(cfg["files"], root)
    label_col = cfg["label_column"]
    counts = count_labels(files, label_col)
    # Oversample slightly in pass 2, then trim exactly.
    keep_p = (1.2 * max_per_label / counts).clip(upper=1.0).to_dict()
    rng = np.random.default_rng(seed)
    kept = []
    for f in files:
        for chunk in _read(f, chunksize=500_000):
            norm = chunk[label_col].map(normalize_label)
            p = norm.map(keep_p).to_numpy(dtype=float)
            mask = rng.random(len(chunk)) < p
            kept.append(chunk.loc[mask])
    df = pd.concat(kept, ignore_index=True)
    df["label_norm"] = df[label_col].map(normalize_label)
    df = df.iloc[rng.permutation(len(df))]
    df = df[df.groupby("label_norm").cumcount() < max_per_label].reset_index(drop=True)
    stats = {"files": [str(f) for f in files], "raw_label_counts": counts.to_dict()}
    return df, stats


def harmonize(df: pd.DataFrame, cfg: dict, taxonomy: Taxonomy) -> pd.DataFrame:
    label_col = cfg["label_column"]
    out = df.drop(columns=[c for c in cfg.get("drop_columns", []) if c in df.columns])
    out = out.rename(columns={label_col: "label_raw"})
    if "label_norm" not in out:
        out["label_norm"] = out["label_raw"].map(normalize_label)
    # Rate features divide by zero duration in some exports: store +/-inf as missing.
    num = [c for c in out.columns if c not in ("label_raw", "label_norm") and pd.api.types.is_float_dtype(out[c])]
    out[num] = out[num].replace([np.inf, -np.inf], np.nan)
    fam = taxonomy.map_labels(out["label_raw"], cfg["taxonomy"])
    out["family"] = fam["family"]
    out["subfamily"] = fam["subfamily"]
    return out


def deduplicate(df: pd.DataFrame, mode: str = "drop_conflicts") -> tuple[pd.DataFrame, dict]:
    """Handle exact duplicate feature rows.

    drop_conflicts (default): same features + same label -> keep one copy; same features with
        different labels -> drop every copy (label noise that cannot be resolved).
    majority: conflicting groups keep only rows of their most frequent label (ties dropped),
        then same-label duplicates are reduced to one copy.
    none: keep every row (sensitivity analysis).
    """
    if mode == "none":
        return df.reset_index(drop=True), {"dedup_mode": mode, "rows_before_dedup": int(len(df)),
                                           "dropped_same_label_duplicates": 0,
                                           "dropped_conflicting_label_rows": 0, "rows_after_dedup": int(len(df))}
    feats = feature_columns(df)
    h = pd.util.hash_pandas_object(df[feats], index=False)
    labels_per_hash = df.groupby(h)["label_norm"].nunique()
    conflicting = set(labels_per_hash[labels_per_hash > 1].index)
    is_conflict = h.isin(conflicting)
    if mode == "majority":
        sub = pd.DataFrame({"h": h[is_conflict], "lab": df.loc[is_conflict, "label_norm"]})
        cnt = sub.groupby(["h", "lab"]).size().reset_index(name="n")
        top = cnt.sort_values("n", ascending=False).groupby("h").head(2)
        tie = top.groupby("h")["n"].apply(lambda s: len(s) > 1 and s.iloc[0] == s.iloc[1])
        winner = cnt.sort_values("n", ascending=False).drop_duplicates("h").set_index("h")["lab"]
        winner = winner[~winner.index.isin(tie[tie].index)]
        keep_conf = is_conflict & (df["label_norm"] == h.map(winner))
        drop_conf = is_conflict & ~keep_conf
        out = df.loc[~drop_conf].copy()
        hh = h[~drop_conf]
        out = out.loc[~hh.duplicated(keep="first").to_numpy()].reset_index(drop=True)
        return out, {"dedup_mode": mode, "rows_before_dedup": int(len(df)),
                     "dropped_conflicting_label_rows": int(drop_conf.sum()),
                     "rows_after_dedup": int(len(out))}
    if mode != "drop_conflicts":
        raise ValueError(f"unknown dedup mode {mode!r}")
    dup_same = h.duplicated(keep="first") & ~is_conflict
    out = df.loc[~is_conflict & ~dup_same].reset_index(drop=True)
    return out, {"dedup_mode": mode,
        "rows_before_dedup": int(len(df)),
        "dropped_same_label_duplicates": int(dup_same.sum()),
        "dropped_conflicting_label_rows": int(is_conflict.sum()),
        "rows_after_dedup": int(len(out)),
    }


def assign_partitions(df: pd.DataFrame, fractions: tuple[float, float, float], seed: int) -> pd.DataFrame:
    """Stratified (per raw label) train/val/test assignment."""
    if abs(sum(fractions) - 1.0) > 1e-9:
        raise ValueError("fractions must sum to 1")
    rng = np.random.default_rng(seed)
    part = np.empty(len(df), dtype=object)
    for _, idx in df.groupby("label_norm").indices.items():
        idx = rng.permutation(idx)
        n = len(idx)
        n_tr = int(round(fractions[0] * n))
        n_va = int(round(fractions[1] * n))
        part[idx[:n_tr]] = "train"
        part[idx[n_tr:n_tr + n_va]] = "val"
        part[idx[n_tr + n_va:]] = "test"
    out = df.copy()
    out["part"] = part
    out.insert(0, "row_id", np.arange(len(out)))
    return out


def prepare_dataset(name: str, cfg: dict, taxonomy: Taxonomy, root: Path, out_dir: Path,
                    max_per_label: int, seed: int,
                    fractions: tuple[float, float, float] = (0.6, 0.2, 0.2),
                    dedup: str = "drop_conflicts", time_col: str | None = None, tag: str = "") -> Path:
    """Prepare one dataset. With `time_col`, that raw column (normally dropped as an identifier) is
    written to a sidecar `<stem>.time.parquet` keyed by row_id, for time-ordered analyses only; it never
    enters the feature set, and the main parquet is unchanged."""
    raw, stats = load_capped(cfg, root, max_per_label, seed)
    if time_col:
        raw["_t_start"] = raw[time_col]
    df = harmonize(raw, cfg, taxonomy)
    df, dstats = deduplicate(df, dedup)
    df = assign_partitions(df, fractions, seed)
    sidecar = df[["row_id", "_t_start"]] if time_col else None
    if time_col:
        df = df.drop(columns=["_t_start"])
    feats = feature_columns(df)
    stats.update(dstats)
    stats.update({
        "dataset": name,
        "feature_space": cfg["feature_space"],
        "seed": seed,
        "max_per_label": max_per_label,
        "fractions": list(fractions),
        "n_features": len(feats),
        "features": feats,
        "non_numeric_features": [c for c in feats if not pd.api.types.is_numeric_dtype(df[c])],
        "missing_values_per_feature": {c: int(n) for c, n in df[feats].isna().sum().items() if n},
        "rows_per_family_part": df.groupby(["family", "part"]).size().unstack(fill_value=0).to_dict(orient="index"),
        "rows_per_subfamily": df["subfamily"].value_counts().to_dict(),
    })
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{name}__cap{max_per_label}__seed{seed}{tag}"
    path = out_dir / f"{stem}.parquet"
    if sidecar is not None:
        sidecar.to_parquet(out_dir / f"{stem}.time.parquet", index=False)
        if path.exists():  # main data already prepared: keep it untouched, only add the sidecar
            existing = pd.read_parquet(path, columns=["row_id", "label_norm"])
            if not (existing["label_norm"].tolist() == df["label_norm"].tolist()
                    and existing["row_id"].tolist() == df["row_id"].tolist()):
                raise RuntimeError(f"{path}: regenerated rows do not match; sidecar would be misaligned")
            return path
    df.to_parquet(path, index=False)
    (out_dir / f"{stem}.stats.json").write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")
    return path
