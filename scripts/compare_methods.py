"""Compare methods on the same splits at the same warm-up false-alarm budget.

Usage: python scripts/compare_methods.py --rule target_warmup_far0.01 --contamination 0 --out results/x.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SOURCES = {
    "RF-MSP (full train)": "results/rf_msp_full_family_seed0.csv",
    "RF-MSP (2k/unit)": "results/rf_msp_cap2000_family_seed0.csv",
    "L1 tiny-local (no pretraining)": "results/l1_tiny-local_family_seed0.csv",
    "L1 DistilBERT": "results/l1_distilbert_family_seed0.csv",
    "L1 SecBERT": "results/l1_secbert_family_seed0.csv",
}
METRICS = ["auroc_ood", "fpr_at_95tpr", "unknown_recall", "unknown_flagged_malicious",
           "benign_rejected_as_unknown", "benign_as_known_attack", "known_macro_f1", "open_set_macro_f1"]


def load(rule: str, contamination: float) -> pd.DataFrame:
    frames = []
    for name, rel in SOURCES.items():
        p = ROOT / rel
        if not p.exists():
            continue
        d = pd.read_csv(p)
        d = d[d["calibration"] == rule]
        if "warmup_contamination" in d:
            c = d["warmup_contamination"].round(3)
            d = d[c.isna() | (c == round(contamination, 3))]
        if "norm" in d:
            d = d[d["norm"] == "none"]
        if "score" not in d:
            d = d.assign(score="msp")
        d = d.assign(method_name=name)
        frames.append(d)
    return pd.concat(frames, ignore_index=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", default="target_warmup_far0.01")
    ap.add_argument("--contamination", type=float, default=0.0, help="warm-up contamination to report")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    d = load(a.rule, a.contamination)
    # Only splits present for every method, so means are comparable.
    common = set.intersection(*(set(g["split_id"]) for _, g in d.groupby("method_name")))
    d = d[d["split_id"].isin(common)]
    cols = [c for c in METRICS if c in d] + (["ms_per_flow"] if "ms_per_flow" in d else [])
    summary = (d.groupby(["protocol", "method_name", "score"], sort=False)[cols].mean().round(3))
    per_split = d.pivot_table(index=["protocol", "source", "holdout"], columns=["method_name", "score"],
                              values="auroc_ood").round(3)
    text = (f"# Method comparison — rule `{a.rule}`, warm-up contamination {a.contamination:g}, "
            f"{len(common)} common splits\n\n"
            f"## Means\n\n```\n{summary.to_string()}\n```\n\n"
            f"## AUROC-OOD per split\n\n```\n{per_split.to_string()}\n```\n")
    print(text)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
