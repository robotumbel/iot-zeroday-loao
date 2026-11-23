"""CPU experiments requested in the first-round review (IEEE Access, Nov 2026).

  --exp temporal   (E1)  time-ordered vs random warm-up windows evaluated on the SAME later test flows
  --exp twostage   (E2)  total-alert control: RF alone, RF with a total-alert budget, and a two-stage
                         detector (benign-only autoencoder gate, RF labels the alerts)
  --exp robust     (E13) robust window rules under zero-day contamination: trimmed quantile,
                         median over several windows, window filtered by the RF's own predictions
  --exp popen      (E7)  P3 without filtering the target: every target unit is kept, units unseen in
                         the source count as unknown (several unknown families at once)
  --exp chrono     (E10) P1 with chronological partitions inside each family (earliest 60% train,
                         next 20% validation, latest 20% test), so neighbouring flows of one campaign
                         cannot fall on both sides of the train/test boundary

Detector: RF (100 trees, MSP), as in the paper; the autoencoder is the benign-only one of
scripts/run_anomaly.py. One CSV row per split x condition x rule.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_baseline_rf as rfb  # noqa: E402
from run_anomaly import AE, Prep  # noqa: E402
from loao.adaptation import make_warmup  # noqa: E402
from loao.calibration import Threshold, target_warmup_far  # noqa: E402
from loao.data import feature_columns  # noqa: E402
from loao.metrics import BENIGN, UNKNOWN, open_set_report, threshold_free  # noqa: E402
from loao.splits import SplitSpec, build_split, load_split  # noqa: E402

FARS = (0.01, 0.05)


def feats_of(df: pd.DataFrame) -> list[str]:
    return [c for c in feature_columns(df) if pd.api.types.is_numeric_dtype(df[c])]


def extra_metrics(true_unit: np.ndarray, pred: np.ndarray, known: set[str]) -> dict:
    t = np.asarray(true_unit, dtype=object)
    p = np.asarray(pred, dtype=object)
    k = np.isin(t, list(known))
    return {"known_attack_detected": float(np.mean(p[k] != BENIGN)) if k.any() else np.nan,
            "known_attack_correct": float(np.mean(p[k] == t[k])) if k.any() else np.nan}


def quantile_threshold(scores: np.ndarray, alpha: float, rule: str) -> Threshold:
    th = target_warmup_far(scores, alpha)
    return Threshold(rule, th.value, th.strict)


def report(split, pred, rule, cond, base) -> dict:
    u = split.unit_col
    r = dict(base, condition=cond, calibration=rule)
    r.update(open_set_report(split.test[u].to_numpy(), pred, split.spec.holdout))
    r.update(extra_metrics(split.test[u].to_numpy(), pred, set(split.known_units)))
    return r


def base_row(split, exp, seed) -> dict:
    return {"split_id": split.spec.split_id, **asdict(split.spec), "exp": exp, "seed_run": seed,
            "n_train": len(split.train), "n_test": len(split.test),
            "n_test_unknown": int((split.test[split.unit_col] == split.spec.holdout).sum())}


# ---------------------------------------------------------------- E1 temporal control
def exp_temporal(manifest: Path, seed: int) -> list[dict]:
    split = load_split(manifest)
    split.manifest_path = manifest
    u = split.unit_col
    full_test = split.test
    pool_all = split.target_pool
    rfb.temporal_restrict(split)  # split.test = later 70%, split.target_pool = earliest 30%
    if split.spec.holdout and (split.test[u] == split.spec.holdout).sum() < 30:
        return []
    rf = rfb.fit_rf(split.train, u, seed)
    score, closed = rfb.msp_score(rf, split.test)
    base = base_row(split, "temporal", seed)
    base.update(threshold_free(split.y_test_unknown.to_numpy(), score))
    # Composition of the later test set vs the full random test set (benign flows labelled as a known attack).
    for name, df in (("late", split.test), ("full", full_test)):
        b = df[df[u] == BENIGN]
        _, cb = rfb.msp_score(rf, b)
        base[f"benign_as_attack_closedset_{name}"] = float(np.mean(cb != BENIGN))
        base[f"n_benign_{name}"] = len(b)
    rows = []
    for c in (0.0, 0.05):
        for cond, pool in (("window_early", split.target_pool), ("window_random", pool_all)):
            w, _ = make_warmup(pool, u, 2000, c, seed)
            s_w = rfb.msp_score(rf, w)[0]
            for a in FARS:
                th = target_warmup_far(s_w, a)
                pred = np.where(th.flags(score), UNKNOWN, closed)
                rows.append(report(split, pred, th.rule, f"{cond}|c={c}", base))
    return rows


# ---------------------------------------------------------------- E2 two-stage / total-alert budget
def exp_twostage(manifest: Path, seed: int) -> list[dict]:
    split = load_split(manifest)
    u = split.unit_col
    f = feats_of(split.train)
    X = lambda d: d[f].to_numpy(dtype=float)  # noqa: E731
    rf = rfb.fit_rf(split.train, u, seed)
    ben = split.train[split.train[u] == BENIGN]
    prep = Prep().fit(X(ben))
    ae = AE(len(f), seed).fit(prep(X(ben)))
    bi = list(rf.classes_).index(BENIGN)

    def scores(d):
        p = rf.predict_proba(X(d))
        return {"msp": 1 - p.max(1), "alert": 1 - p[:, bi], "ae": ae.score(prep(X(d))),
                "pred": rf.classes_[p.argmax(1)]}

    st = scores(split.test)
    base = base_row(split, "twostage", seed)
    rows = []
    for c in (0.0, 0.05):
        w, _ = make_warmup(split.target_pool, u, 2000, c, seed)
        sw = scores(w)
        for a in FARS:
            t_msp = target_warmup_far(sw["msp"], a)
            t_alert = target_warmup_far(sw["alert"], a)
            t_ae = target_warmup_far(sw["ae"], a)
            # (a) paper rule: unknown if MSP above the budget threshold, otherwise RF label
            pa = np.where(t_msp.flags(st["msp"]), UNKNOWN, st["pred"])
            # (b) RF with a total-alert budget: alert if P(benign) is low enough; alerted flows get the RF
            #     attack label unless MSP flags them (or the RF still prefers benign), then UNKNOWN
            alert = t_alert.flags(st["alert"])
            lab = np.where(t_msp.flags(st["msp"]) | (st["pred"] == BENIGN), UNKNOWN, st["pred"])
            pb = np.where(alert, lab, BENIGN)
            # (c) two-stage: benign-only AE gate decides alert vs benign; RF names the alerted flows
            gate = t_ae.flags(st["ae"])
            pc = np.where(gate, lab, BENIGN)
            for rule, pred in (("rf_unknown_budget", pa), ("rf_total_alert_budget", pb), ("ae_gate_rf_label", pc)):
                rows.append(report(split, pred, f"{rule}{a:g}", f"c={c}", base))
    return rows


# ---------------------------------------------------------------- E13 robust windows
def exp_robust(manifest: Path, seed: int) -> list[dict]:
    split = load_split(manifest)
    u = split.unit_col
    rf = rfb.fit_rf(split.train, u, seed)
    score, closed = rfb.msp_score(rf, split.test)
    base = base_row(split, "robust", seed)
    h = split.spec.holdout
    rows = []
    for c in (0.0, 0.05, 0.2):
        src = "holdout" if c > 0 else "all"
        w, _ = make_warmup(split.target_pool, u, 2000, c, seed, src, h)
        s_w, p_w = rfb.msp_score(rf, w)
        # five windows for the median rule; only the first one is contaminated (a burst)
        others = [rfb.msp_score(rf, make_warmup(split.target_pool, u, 2000, 0.0, seed + 100 + j)[0])[0]
                  for j in range(4)]
        for a in FARS:
            ths = [target_warmup_far(s_w, a)]
            for rho in (0.05, 0.2):  # drop the top rho share of window scores, then the alpha quantile
                keep = np.sort(s_w)[: int(np.floor(len(s_w) * (1 - rho)))]
                ths.append(quantile_threshold(keep, a, f"trimmed{rho:g}_far{a:g}"))
            med = float(np.median([target_warmup_far(s, a).value for s in [s_w, *others]]))
            ths.append(Threshold(f"median5_far{a:g}", med, True))
            filt = s_w[p_w == BENIGN]  # window flows the RF itself labels benign
            if len(filt) >= 200:
                ths.append(quantile_threshold(filt, a, f"rf_filtered_far{a:g}"))
            for th in ths:
                pred = np.where(th.flags(score), UNKNOWN, closed)
                rows.append(report(split, pred, th.rule, f"holdout_c={c}", base))
    return rows


# ---------------------------------------------------------------- E7 unfiltered P3
def exp_popen(manifest: Path, seed: int) -> list[dict]:
    split = load_split(manifest)
    if split.spec.protocol != "P3":
        return []
    m = json.loads(manifest.read_text(encoding="utf-8"))
    tgt = pd.read_parquet(m["processed_files"][split.spec.target])
    u = split.unit_col
    f = feats_of(split.train)
    test = tgt[tgt["part"] == "test"]
    src_hash = set(pd.util.hash_pandas_object(split.train[feature_columns(split.train)], index=False))
    test = test[~pd.util.hash_pandas_object(test[feature_columns(split.train)], index=False).isin(src_hash).to_numpy()]
    pool = tgt[tgt["part"] == "val"]
    known = set(split.known_units)
    is_unk = (~test[u].isin(known | {BENIGN})).to_numpy()
    rf = rfb.fit_rf(split.train, u, seed)
    score, closed = rfb.msp_score(rf, test)
    X = lambda d: d[f].to_numpy(dtype=float)  # noqa: E731
    ben = split.train[split.train[u] == BENIGN]
    prep = Prep().fit(X(ben))
    ae = AE(len(f), seed).fit(prep(X(ben)))
    s_ae = ae.score(prep(X(test)))
    unknown_units = sorted(set(test[u][is_unk]))
    base = {"split_id": split.spec.split_id, **asdict(split.spec), "exp": "popen", "seed_run": seed,
            "n_test": len(test), "n_test_unknown": int(is_unk.sum()), "unknown_units": json.dumps(unknown_units)}
    rows = []
    for det, s in (("RF-MSP", score), ("AE", s_ae)):
        tf = threshold_free(is_unk.astype(int), s, (test[u] == BENIGN).to_numpy())
        w, _ = make_warmup(pool, u, 2000, 0.0, seed)
        s_w = rfb.msp_score(rf, w)[0] if det == "RF-MSP" else ae.score(prep(X(w)))
        for a in FARS:
            th = target_warmup_far(s_w, a)
            flag = th.flags(s)
            pred = np.where(flag, UNKNOWN, closed if det == "RF-MSP" else BENIGN)
            ben_m = (test[u] == BENIGN).to_numpy()
            r = dict(base, **tf, detector=det, calibration=th.rule,
                     unknown_recall=float(flag[is_unk].mean()),
                     unknown_flagged_malicious=float((pred[is_unk] != BENIGN).mean()),
                     benign_rejected_as_unknown=float(flag[ben_m].mean()),
                     benign_false_alarm_rate=float((pred[ben_m] != BENIGN).mean()))
            for un in unknown_units:
                mm = (test[u] == un).to_numpy()
                r[f"recall_{un}"] = float(flag[mm].mean())
            rows.append(r)
    return rows


# ---------------------------------------------------------------- E10 chronological partitions
def chrono_parts(df: pd.DataFrame, times: pd.Series, unit: str) -> pd.DataFrame:
    df = df.copy()
    t = df["row_id"].map(times)
    q = t.groupby(df[unit]).rank(pct=True, method="first")
    df["part"] = np.where(q <= 0.6, "train", np.where(q <= 0.8, "val", "test"))
    return df


def exp_chrono(manifest: Path, seed: int) -> list[dict]:
    m = json.loads(manifest.read_text(encoding="utf-8"))
    spec = SplitSpec(**m["spec"])
    if spec.protocol != "P1":
        return []
    path = Path(m["processed_files"][spec.source])
    df = pd.read_parquet(path)
    times = pd.read_parquet(path.with_suffix(".time.parquet")).set_index("row_id")["_t_start"]
    df = chrono_parts(df, times, spec.level)
    try:
        split = build_split(spec, {spec.source: df})
    except ValueError:
        return []
    u = split.unit_col
    rf = rfb.fit_rf(split.train, u, seed)
    score, closed = rfb.msp_score(rf, split.test)
    f = feats_of(split.train)
    X = lambda d: d[f].to_numpy(dtype=float)  # noqa: E731
    ben = split.train[split.train[u] == BENIGN]
    prep = Prep().fit(X(ben))
    ae = AE(len(f), seed).fit(prep(X(ben)))
    s_ae = ae.score(prep(X(split.test)))
    base = base_row(split, "chrono", seed)
    rows = []
    w, _ = make_warmup(split.target_pool, u, 2000, 0.0, seed)
    for det, s, cl, sw in (("RF-MSP", score, closed, rfb.msp_score(rf, w)[0]),
                           ("AE", s_ae, np.full(len(split.test), BENIGN, dtype=object), ae.score(prep(X(w))))):
        b = dict(base, detector=det)
        b.update(threshold_free(split.y_test_unknown.to_numpy(), s, (split.test[u] == BENIGN).to_numpy()))
        for a in FARS:
            th = target_warmup_far(sw, a)
            pred = np.where(th.flags(s), UNKNOWN, cl)
            rows.append(report(split, pred, th.rule, "chrono", b))
    return rows


EXPS = {"temporal": exp_temporal, "twostage": exp_twostage, "robust": exp_robust, "popen": exp_popen,
        "chrono": exp_chrono}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", required=True, choices=sorted(EXPS))
    ap.add_argument("--splits", required=True)
    ap.add_argument("--only", nargs="*", default=["P1__", "P3__"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n-estimators", type=int, default=100)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rfb.N_ESTIMATORS = a.n_estimators
    index = pd.read_csv(Path(a.splits) / "index.csv")
    ids = index.loc[index["status"] == "ok", "split_id"]
    ids = ids[ids.apply(lambda s: any(o in s for o in a.only))]
    rows = []
    for sid in ids:
        res = EXPS[a.exp](Path(a.splits) / f"{sid}.json", a.seed)
        rows += res
        print(f"{a.exp} {sid}: {len(res)} rows", flush=True)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)


if __name__ == "__main__":
    main()
