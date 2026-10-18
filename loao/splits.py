"""Evaluation protocols.

P1  within-dataset LOAO   : train on A without unit k, test on A (k is the unknown).
P2  cross-dataset closed  : train on A, test on B restricted to units known in A.
P3  cross-dataset LOAO    : train on A without unit k, test on B (k is the unknown).

A "unit" is a family (far-OOD) or a subfamily (near-OOD), chosen with `level`.
Splits are defined by the processed dataset (row_id + part columns) and a SplitSpec,
so they are reproducible without storing index lists.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pandas as pd

from .data import feature_columns
from .taxonomy import BENIGN, LEVELS


@dataclass(frozen=True)
class SplitSpec:
    protocol: str
    source: str
    target: str
    level: str
    holdout: str | None
    seed: int

    @property
    def split_id(self) -> str:
        h = self.holdout or "none"
        return f"{self.protocol}__{self.source}__to__{self.target}__{self.level}={h}__seed{self.seed}"


@dataclass
class Split:
    spec: SplitSpec
    train: pd.DataFrame
    val: pd.DataFrame
    test: pd.DataFrame
    known_units: list[str]
    pseudo_unknown_units: list[str]
    # Target-network flows outside the test partition (its 'val' part). Methods may use them
    # only WITHOUT labels, e.g. as a warm-up window; labels stay for building the simulation.
    target_pool: pd.DataFrame = field(default_factory=pd.DataFrame)
    report: dict = field(default_factory=dict)

    @property
    def unit_col(self) -> str:
        return self.spec.level

    @property
    def y_test_unknown(self) -> pd.Series:
        """1 for flows of the held-out unit, 0 for benign and known attacks."""
        if self.spec.holdout is None:
            return pd.Series(0, index=self.test.index)
        return (self.test[self.unit_col] == self.spec.holdout).astype(int)

    def calibration_fold(self, pseudo_unit: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Nested calibration: treat a known unit as pseudo-unknown.

        Returns (train_without_pseudo, cal_in, cal_out), all from the SOURCE dataset only.
        The real held-out unit is never present.
        """
        if pseudo_unit not in self.pseudo_unknown_units:
            raise ValueError(f"{pseudo_unit!r} is not an eligible pseudo-unknown unit")
        u = self.unit_col
        tr = self.train[self.train[u] != pseudo_unit]
        cal_in = self.val[self.val[u] != pseudo_unit]
        cal_out = self.val[self.val[u] == pseudo_unit]
        return tr, cal_in, cal_out


def _units(df: pd.DataFrame, level: str, part: str | None = None, min_rows: int = 1) -> set[str]:
    d = df if part is None else df[df["part"] == part]
    vc = d[level].value_counts()
    return {u for u, n in vc.items() if n >= min_rows and u != BENIGN}


def _row_hash(df: pd.DataFrame, feats: list[str]) -> pd.Series:
    return pd.util.hash_pandas_object(df[feats], index=False)


def build_split(spec: SplitSpec, datasets: dict[str, pd.DataFrame], min_unit_rows: int = 30) -> Split:
    if spec.level not in LEVELS:
        raise ValueError(f"level must be one of {LEVELS}")
    src, tgt = datasets[spec.source], datasets[spec.target]
    u = spec.level
    feats_src, feats_tgt = feature_columns(src), feature_columns(tgt)
    if spec.source != spec.target and feats_src != feats_tgt:
        raise ValueError(
            f"Feature spaces differ between {spec.source} and {spec.target}; "
            "cross-dataset protocols need an identical feature set (e.g. NetFlow v3)."
        )

    train = src[(src["part"] == "train") & (src[u] != spec.holdout)]
    val = src[(src["part"] == "val") & (src[u] != spec.holdout)]
    known = sorted(set(train[u].unique()) - {BENIGN})

    test = tgt[tgt["part"] == "test"]
    allowed = set(known) | {BENIGN} | ({spec.holdout} if spec.holdout else set())
    dropped_units = sorted(set(test[u].unique()) - allowed)
    test = test[test[u].isin(allowed)]
    target_pool = tgt[(tgt["part"] == "val") & tgt[u].isin(allowed)]

    report: dict = {"dropped_target_units_not_in_source": dropped_units}

    # Cross-dataset leakage guard: identical feature rows in source train and target test.
    if spec.source != spec.target:
        overlap = _row_hash(test, feats_tgt).isin(set(_row_hash(train, feats_src)))
        report["removed_test_rows_identical_to_source_train"] = int(overlap.sum())
        test = test[~overlap.to_numpy()]

    # Hard checks.
    if spec.holdout is not None:
        assert spec.holdout not in set(train[u]) and spec.holdout not in set(val[u]), "held-out unit leaked"
        n_unknown = int((test[u] == spec.holdout).sum())
        if n_unknown < min_unit_rows:
            raise ValueError(f"{spec.split_id}: only {n_unknown} unknown test rows (< {min_unit_rows})")
    if not known:
        raise ValueError(f"{spec.split_id}: no known attack unit left for training")
    assert set(train["row_id"]).isdisjoint(set(test["row_id"])) or spec.source != spec.target
    assert set(target_pool["row_id"]).isdisjoint(set(test["row_id"])), "warm-up pool overlaps test"

    val_units = val[u].value_counts()
    pseudo = sorted(k for k in known if val_units.get(k, 0) >= min_unit_rows)

    report.update({
        "n_train": int(len(train)), "n_val": int(len(val)), "n_test": int(len(test)),
        "n_target_pool": int(len(target_pool)),
        "n_test_unknown": int((test[u] == spec.holdout).sum()) if spec.holdout else 0,
        "train_units": train[u].value_counts().to_dict(),
        "test_units": test[u].value_counts().to_dict(),
        "known_units": known,
        "pseudo_unknown_units": pseudo,
    })
    return Split(spec, train, val, test, known, pseudo, target_pool, report)


def enumerate_specs(datasets: dict[str, pd.DataFrame], feature_spaces: dict[str, str],
                    protocols: list[str], level: str, seed: int,
                    min_unit_rows: int = 30, include_target_only_unknowns: bool = False) -> list[SplitSpec]:
    specs: list[SplitSpec] = []
    names = sorted(datasets)
    if "P1" in protocols:
        for d in names:
            units = _units(datasets[d], level, "test", min_unit_rows)
            for k in sorted(units):
                if len(_units(datasets[d], level, "train") - {k}) >= 1:
                    specs.append(SplitSpec("P1", d, d, level, k, seed))
    pairs = [(a, b) for a, b in itertools.permutations(names, 2) if feature_spaces[a] == feature_spaces[b]]
    if "P2" in protocols:
        specs += [SplitSpec("P2", a, b, level, None, seed) for a, b in pairs]
    if "P3" in protocols:
        for a, b in pairs:
            src_units = _units(datasets[a], level, "train")
            tgt_units = _units(datasets[b], level, "test", min_unit_rows)
            cands = tgt_units if include_target_only_unknowns else (src_units & tgt_units)
            for k in sorted(cands):
                if len(src_units - {k}) >= 1:
                    specs.append(SplitSpec("P3", a, b, level, k, seed))
    return specs


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write_manifests(specs: list[SplitSpec], datasets: dict[str, pd.DataFrame],
                    processed_files: dict[str, Path], out_dir: Path, min_unit_rows: int = 30) -> pd.DataFrame:
    """Build every split once, write one JSON manifest per split and an index CSV."""
    out_dir.mkdir(parents=True, exist_ok=True)
    hashes = {n: file_sha256(p) for n, p in processed_files.items()}
    rows = []
    for spec in specs:
        try:
            split = build_split(spec, datasets, min_unit_rows)
            status, rep = "ok", split.report
        except ValueError as e:
            status, rep = "skipped", {"reason": str(e)}
        manifest = {
            "spec": asdict(spec), "split_id": spec.split_id, "status": status,
            "processed_files": {spec.source: Path(processed_files[spec.source]).as_posix(),
                                spec.target: Path(processed_files[spec.target]).as_posix()},
            "processed_sha256": {spec.source: hashes[spec.source], spec.target: hashes[spec.target]},
            "report": rep,
        }
        (out_dir / f"{spec.split_id}.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
        rows.append({**asdict(spec), "split_id": spec.split_id, "status": status,
                     "n_train": rep.get("n_train"), "n_test": rep.get("n_test"),
                     "n_test_unknown": rep.get("n_test_unknown"), "reason": rep.get("reason", "")})
    index = pd.DataFrame(rows)
    index.to_csv(out_dir / "index.csv", index=False)
    return index


def load_split(manifest_path: Path, min_unit_rows: int = 30) -> Split:
    """Rebuild a split from its manifest and verify the processed files are unchanged."""
    m = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    datasets = {}
    for name, p in m["processed_files"].items():
        p = Path(p.replace("\\", "/"))  # manifests written on Windows may use backslashes
        if file_sha256(p) != m["processed_sha256"][name]:
            raise RuntimeError(f"{p} changed since the manifest was written")
        datasets[name] = pd.read_parquet(p)
    return build_split(SplitSpec(**m["spec"]), datasets, min_unit_rows)
