"""Reference baseline: Random Forest + maximum softmax probability (MSP) unknown score.

Threshold rules (source data only, never the real held-out unit), see loao/calibration.py:
  pseudo : nested pseudo-unknown folds, Youden-J threshold averaged over folds.
  far    : fixed false-alarm budget on benign validation flows (default 1% and 5%).
  warmup : same budget on an unlabeled warm-up window from the target network (loao/adaptation.py).
Feature normalisation (--norm): none, or per_network = rank transform fitted on each network's own
warm-up window. One output row per split x contamination x normalisation x rule.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from loao.adaptation import NetworkNormalizer, make_warmup  # noqa: E402
from loao.calibration import Threshold, benign_far, pseudo_youden, target_warmup_far  # noqa: E402
from loao.data import feature_columns  # noqa: E402
from loao.serialize import Discretizer  # noqa: E402
from loao.metrics import BENIGN, UNKNOWN, open_set_report, threshold_free  # noqa: E402
from loao.splits import load_split  # noqa: E402


def numeric(df: pd.DataFrame) -> np.ndarray:
    feats = [c for c in feature_columns(df) if pd.api.types.is_numeric_dtype(df[c])]
    return df[feats].to_numpy(dtype=float)


N_ESTIMATORS = 200


def fit_rf(df: pd.DataFrame, unit: str, seed: int) -> RandomForestClassifier:
    rf = RandomForestClassifier(n_estimators=N_ESTIMATORS, n_jobs=-1, random_state=seed, class_weight="balanced")
    rf.fit(numeric(df), df[unit].to_numpy())
    return rf


def msp_score(rf: RandomForestClassifier, df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    proba = rf.predict_proba(numeric(df))
    return 1.0 - proba.max(axis=1), rf.classes_[proba.argmax(axis=1)]


def cap_per_unit(df: pd.DataFrame, unit: str, n: int, seed: int) -> pd.DataFrame:
    if n <= 0:
        return df
    df = df.iloc[np.random.default_rng(seed).permutation(len(df))]
    return df[df.groupby(unit).cumcount() < n]


def temporal_restrict(split, cut_quantile: float = 0.3):
    """Time-ordered evaluation: warm-up only from target traffic before the cut, test only after it.

    Flow start times come from the `<processed>.time.parquet` sidecar (they are never features).
    """
    m = json.loads(Path(split.manifest_path).read_text(encoding="utf-8"))
    tgt_file = Path(m["processed_files"][split.spec.target].replace("\\", "/"))
    times = pd.read_parquet(tgt_file.with_suffix(".time.parquet")).set_index("row_id")["_t_start"]
    t_pool = split.target_pool["row_id"].map(times)
    t_test = split.test["row_id"].map(times)
    cut = float(np.nanquantile(np.r_[t_pool.to_numpy(float), t_test.to_numpy(float)], cut_quantile))
    split.target_pool = split.target_pool[(t_pool <= cut).to_numpy()]
    split.test = split.test[(t_test > cut).to_numpy()]
    return cut


def run(manifest: Path, rules: list[str], fars: list[float], norms: list[str],
        warmup_sizes: list[int], contaminations: list[float], seed: int, max_train_per_unit: int = 0,
        discretize: int = 0, attack_sources: tuple[str, ...] = ("all",), temporal: bool = False) -> list[dict]:
    split = load_split(manifest)
    split.manifest_path = manifest
    u = split.unit_col
    split.train = cap_per_unit(split.train, u, max_train_per_unit, seed)
    extra = {"discretize": discretize, "temporal": temporal}
    if temporal:
        extra["temporal_cut_ms"] = temporal_restrict(split)
    if discretize:
        feats = [c for c in feature_columns(split.train) if pd.api.types.is_numeric_dtype(split.train[c])]
        disc = Discretizer(discretize).fit(split.train[feats])
        for name in ("train", "val", "test", "target_pool"):
            df = getattr(split, name).copy()
            df[feats] = disc.transform(df[feats])
            setattr(split, name, df)
    same_net = split.spec.source == split.spec.target
    y_unk = split.y_test_unknown.to_numpy()
    if split.spec.holdout and y_unk.sum() < 30:
        return []  # too few unknown flows left (possible after the temporal cut)
    windows = [(c, src, n) for c in contaminations for src in attack_sources for n in warmup_sizes
               if not (src == "holdout" and c == 0.0)]
    rows = []
    for norm in norms:
        c0, s0, n0 = windows[0]
        warm_src, _ = make_warmup(pd.concat([split.train, split.val]), u, n0, c0, seed)
        warm_tgt0, _ = make_warmup(split.target_pool, u, n0, c0, seed, s0, split.spec.holdout)
        if norm == "none":
            f_src = f_tgt = (lambda d: d)
        else:
            n_src = NetworkNormalizer(seed=seed).fit(warm_src)
            n_tgt = n_src if same_net else NetworkNormalizer(seed=seed).fit(warm_tgt0)
            f_src, f_tgt = n_src.transform, n_tgt.transform
        train, val, test = f_src(split.train), f_src(split.val), f_tgt(split.test)
        rf = fit_rf(train, u, seed)

        base_th: list[Threshold] = []
        if "pseudo" in rules and split.pseudo_unknown_units:
            folds = []
            for j in split.pseudo_unknown_units:
                tr, cin, cout = (f_src(d) for d in split.calibration_fold(j))
                rf_j = fit_rf(tr, u, seed)
                folds.append((msp_score(rf_j, cin)[0], msp_score(rf_j, cout)[0]))
            base_th.append(pseudo_youden(folds))
        if "far" in rules:
            s_benign = msp_score(rf, val[val[u] == BENIGN])[0]
            base_th += [benign_far(s_benign, f) for f in fars]

        score, closed_pred = msp_score(rf, test)
        tf = threshold_free(y_unk, score, (test[u] == BENIGN).to_numpy())
        for c, src, nw in windows:
            warm_tgt, winfo = make_warmup(split.target_pool, u, nw, c, seed, src, split.spec.holdout)
            ths = list(base_th)
            if "warmup" in rules:
                s_warm = msp_score(rf, f_tgt(warm_tgt))[0]
                ths += [target_warmup_far(s_warm, f) for f in fars]
            base = {"split_id": split.spec.split_id, **asdict(split.spec), "method": "RF-MSP",
                    "n_train": len(train), "max_train_per_unit": max_train_per_unit, "norm": norm, **extra,
                    **winfo, "n_test": len(test), "n_test_unknown": int(y_unk.sum())}
            base["warmup_attack_units"] = json.dumps(base["warmup_attack_units"])
            base.update(tf)
            for th in ths:
                pred = np.where(th.flags(score), UNKNOWN, closed_pred)
                r = dict(base, calibration=th.rule, threshold=th.value)
                r.update(open_set_report(test[u].to_numpy(), pred, split.spec.holdout))
                rows.append(r)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True, help="folder with split manifests")
    ap.add_argument("--calib", nargs="+", default=["pseudo", "far", "warmup"], choices=["pseudo", "far", "warmup"])
    ap.add_argument("--far", type=float, nargs="+", default=[0.01, 0.05],
                    help="false-alarm budgets for the 'far' and 'warmup' rules")
    ap.add_argument("--norm", nargs="+", default=["none", "per_network"], choices=["none", "per_network"])
    ap.add_argument("--warmup-n", type=int, nargs="+", default=[2000], help="flows in the unlabeled warm-up window")
    ap.add_argument("--contamination", type=float, nargs="+", default=[0.05],
                    help="share of attack flows inside the warm-up window")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="results/rf_msp.csv")
    ap.add_argument("--n-estimators", type=int, default=200)
    ap.add_argument("--only", nargs="*", default=None, help="keep split_ids containing any of these substrings")
    ap.add_argument("--max-train-per-unit", type=int, default=0, help="0 = full training partition")
    ap.add_argument("--discretize", type=int, default=0, help="train/test on N-level quantile bins (0 = off)")
    ap.add_argument("--attack-source", nargs="+", default=["all"], choices=["all", "known", "holdout"],
                    help="which target attacks may contaminate the warm-up window")
    ap.add_argument("--temporal", action="store_true", help="warm-up from early target traffic, test on later traffic")
    a = ap.parse_args()
    global N_ESTIMATORS
    N_ESTIMATORS = a.n_estimators
    index = pd.read_csv(Path(a.splits) / "index.csv")
    rows = []
    ids = index.loc[index["status"] == "ok", "split_id"]
    if a.only:
        ids = ids[ids.apply(lambda s: any(o in s for o in a.only))]
    for sid in ids:
        res = run(Path(a.splits) / f"{sid}.json", a.calib, a.far, a.norm, a.warmup_n, a.contamination, a.seed,
                  a.max_train_per_unit, a.discretize, tuple(a.attack_source), a.temporal)
        rows += res
        for r in res:
            print(f"{sid} [{r['norm']}|c={r['warmup_contamination']:.2f}|{r['calibration']}]: AUROC={r['auroc_ood']:.3f} "
                  f"unk-rec={r.get('unknown_recall', float('nan')):.3f} "
                  f"benign-FA={r['benign_false_alarm_rate']:.3f} open-F1={r['open_set_macro_f1']:.3f}", flush=True)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"-> {out}")


if __name__ == "__main__":
    main()
