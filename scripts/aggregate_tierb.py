"""Summaries of the Tier-B experiments requested in the pre-submission review (seeds 0-2).

Writes results/tierb_summary.md:
  1. warm-up window size and contamination source (RF, results/rf_windows_family_seed*.csv)
  2. time-ordered warm-up (RF, results/rf_temporal_family_seed*.csv)
  3. de-duplication sensitivity (RF, results/rf_dedup{none,majority}_family_seed*.csv)
  4. benign-only anomaly detectors and LightGBM (results/anomaly_family_seed*.csv), with
     AUROC against benign flows recomputed for the neural detectors from their stored scores
Serialization controls (bin5, kv) are covered by scripts/stats_tests.py.
"""

from __future__ import annotations

import glob
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
SEEDS = (0, 1, 2)


def load(pattern: str) -> pd.DataFrame:
    frames = []
    for s in SEEDS:
        p = ROOT / pattern.format(s=s)
        if p.exists():
            frames.append(pd.read_csv(p).assign(seed_run=s))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def ms(g: pd.DataFrame, col: str) -> str:
    s = g.groupby("seed_run")[col].mean()
    return f"{s.mean():.3f} ± {s.std(ddof=1):.3f}" if len(s) > 1 else f"{s.mean():.3f}"


def table(d: pd.DataFrame, by: list[str], cols: list[str]) -> str:
    rows = []
    for key, g in d.groupby(by):
        key = key if isinstance(key, tuple) else (key,)
        rows.append(dict(zip(by, key), **{c: ms(g, c) for c in cols}, n_seeds=g["seed_run"].nunique()))
    return "```\n" + pd.DataFrame(rows).to_string(index=False) + "\n```"


def neural_auroc_vs_benign() -> pd.DataFrame:
    rows = []
    for folder in glob.glob(str(ROOT / "results/scores/*")):
        method = Path(folder).name
        for f in glob.glob(folder + "/*.npz"):
            sid = Path(f).stem
            if not (sid.startswith("P1") or sid.startswith("P3")):
                continue
            z = np.load(f, allow_pickle=True)
            unit = z["test_unit"]
            hold = sid.split("=")[1].split("__")[0]
            seed = int(sid.rsplit("seed", 1)[1])
            m = (unit == hold) | (unit == "BENIGN")
            y = (unit[m] == hold).astype(int)
            for sc in ("maha", "knn"):
                key = f"test_{sc}"
                if key in z.files and y.min() != y.max():
                    rows.append({"method": method, "score": sc, "protocol": sid[:2], "split": sid.rsplit("__seed", 1)[0],
                                 "seed_run": seed, "auroc_unknown_vs_benign": roc_auc_score(y, z[key][m])})
    return pd.DataFrame(rows)


def main() -> None:
    out = ["# Tier-B experiments (seeds 0-2)\n"]

    w = load("results/rf_windows_family_seed{s}.csv")
    if len(w):
        w = w[w["calibration"].str.startswith("target_warmup")]
        out.append("## 1. Warm-up window size (contamination 5%, any target unit), RF full\n")
        sel = w[(w["warmup_attack_source"] == "all") & (w["warmup_contamination"].round(2).between(0.04, 0.06))]
        out.append(table(sel, ["protocol", "calibration", "warmup_requested"],
                         ["benign_rejected_as_unknown", "unknown_recall"]))
        out.append("\n## 1b. Contamination source (window 2,000 flows), RF full\n")
        sel = w[w["warmup_requested"] == 2000].copy()
        sel["c"] = sel["warmup_contamination"].round(2)
        out.append(table(sel, ["protocol", "calibration", "warmup_attack_source", "c"],
                         ["unknown_recall", "benign_rejected_as_unknown", "warmup_holdout_share"]))

    t = load("results/rf_temporal_family_seed{s}.csv")
    if len(t):
        out.append("\n## 2. Time-ordered warm-up (window from the earliest 30% of target traffic, test on the rest)\n")
        out.append(table(t, ["protocol", "calibration"], ["benign_rejected_as_unknown", "unknown_recall",
                                                          "benign_false_alarm_rate"]))
        out.append("\nRandom (exchangeable) windows, same detector, for comparison:\n")
        r = load("results/rf_windows_family_seed{s}.csv")
        r = r[(r["warmup_requested"] == 2000) & (r["warmup_attack_source"] == "all")
              & (r["warmup_contamination"].round(2) == 0.05)]
        out.append(table(r, ["protocol", "calibration"], ["benign_rejected_as_unknown", "unknown_recall",
                                                          "benign_false_alarm_rate"]))

    for mode in ("none", "majority"):
        d = load(f"results/rf_dedup{mode}_family_seed{{s}}.csv")
        if len(d):
            out.append(f"\n## 3. De-duplication = {mode} (RF full, warm-up 1%, clean window)\n")
            d = d[(d["calibration"] == "target_warmup_far0.01") & (d["warmup_contamination"].round(2) == 0)]
            out.append(table(d, ["protocol"], ["auroc_ood", "unknown_recall", "benign_false_alarm_rate"]))
            if mode == "none":
                rr = d[(d["protocol"] == "P1") & d["source"].str.contains("ton") & (d["holdout"] == "RECON")]
                if len(rr):
                    out.append(f"- ToN RECON (P1) without de-duplication: AUROC {ms(rr, 'auroc_ood')}")
    base = load("results/rf_msp_full_family_seed{s}.csv")
    if len(base):
        b = base[(base["calibration"] == "target_warmup_far0.01") & (base["warmup_contamination"].round(2) == 0)]
        out.append("\nDefault (conflicting vectors removed), same detector and rule:\n")
        out.append(table(b, ["protocol"], ["auroc_ood", "unknown_recall", "benign_false_alarm_rate"]))

    a = load("results/anomaly_family_seed{s}.csv")
    if len(a):
        out.append("\n## 4. Benign-only anomaly detectors and LightGBM (warm-up 1%, clean window)\n")
        a1 = a[(a["calibration"] == "target_warmup_far0.01") & (a["warmup_contamination"].round(2) == 0)]
        out.append(table(a1, ["protocol", "method"], ["auroc_ood", "auroc_unknown_vs_benign", "unknown_recall",
                                                      "benign_rejected_as_unknown", "ms_per_flow"]))
        rf = load("results/rf_windows_family_seed{s}.csv")
        if len(rf) and "auroc_unknown_vs_benign" in rf:
            rf = rf.drop_duplicates(["split_id", "seed_run"])
            out.append("\nRF full, AUROC of the held-out unit against benign flows:\n")
            out.append(table(rf, ["protocol"], ["auroc_unknown_vs_benign"]))
        nn = neural_auroc_vs_benign()
        if len(nn):
            out.append("\nNeural detectors, AUROC of the held-out unit against benign flows (from stored scores):\n")
            out.append(table(nn, ["protocol", "method", "score"], ["auroc_unknown_vs_benign"]))

    text = "\n".join(out) + "\n"
    (ROOT / "results/tierb_summary.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
