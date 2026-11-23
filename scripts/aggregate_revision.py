"""Summaries of the first-round revision experiments (seeds 0-2). Writes results/revision_summary.md.

E1 temporal control, E2 total-alert control / two-stage, E5 LightGBM energy, E7 unfiltered P3,
E8 de-duplication sensitivity for MLP and AE, E10 chronological P1, E12 extra baselines,
E13 robust windows, E14 explicit missing-value token. Sections are skipped when files are missing.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results/revision"
SEEDS = (0, 1, 2)


def load(pattern: str) -> pd.DataFrame:
    fr = []
    for s in SEEDS:
        p = R / pattern.format(s=s)
        if p.exists() and p.stat().st_size > 0:
            d = pd.read_csv(p)
            if "seed_run" not in d:
                d["seed_run"] = s
            fr.append(d)
    return pd.concat(fr, ignore_index=True) if fr else pd.DataFrame()


def ms(g: pd.DataFrame, col: str) -> str:
    if col not in g or g[col].isna().all():
        return "-"
    s = g.groupby("seed_run")[col].mean()
    return f"{s.mean():.3f} ± {s.std(ddof=1):.3f}" if len(s) > 1 else f"{s.mean():.3f}"


def table(d: pd.DataFrame, by: list[str], cols: list[str]) -> str:
    rows = []
    for key, g in d.groupby(by, dropna=False):
        key = key if isinstance(key, tuple) else (key,)
        rows.append({**dict(zip(by, key)), **{c: ms(g, c) for c in cols}, "seeds": g["seed_run"].nunique()})
    return "```\n" + pd.DataFrame(rows).to_string(index=False) + "\n```\n"


def main() -> None:
    out = ["# First-round revision experiments (seeds 0-2)\n"]
    core = ["benign_rejected_as_unknown", "benign_false_alarm_rate", "unknown_recall", "unknown_flagged_malicious"]

    d = load("temporal_family_seed{s}.csv")
    if len(d):
        out.append("## E1. Time-ordered vs random windows on the same later test flows (RF)\n")
        out.append(table(d, ["protocol", "condition", "calibration"], core))
        comp = d.drop_duplicates(["split_id", "seed_run"])
        out.append("Benign flows classified as a known attack by the closed-set RF (no threshold), later 70% vs full test:\n")
        out.append(table(comp, ["protocol"], ["benign_as_attack_closedset_late", "benign_as_attack_closedset_full"]))

    d = load("twostage_family_seed{s}.csv")
    if len(d):
        out.append("## E2. Total-alert control (RF; AE gate + RF labels)\n")
        out.append(table(d, ["protocol", "condition", "calibration"], core + ["known_attack_detected", "known_attack_correct"]))

    d = load("lgbm_energy_family_seed{s}.csv")
    if len(d):
        d = d[d["calibration"] == "target_warmup_far0.01"]
        out.append("## E5. LightGBM with an energy score (1% warm-up budget, clean window)\n")
        out.append(table(d, ["protocol"], ["auroc_ood", "auroc_unknown_vs_benign", "unknown_recall", "benign_false_alarm_rate"]))

    d = load("popen_family_seed{s}.csv")
    if len(d):
        out.append("## E7. P3 without filtering target units (every unit unseen in the source is unknown)\n")
        rc = [c for c in d.columns if c.startswith("recall_")]
        d["block"] = d["split_id"].str.replace(r"__seed\d+$", "", regex=True).str.replace("P3__", "")
        d = d[d["calibration"] == "target_warmup_far0.01"]
        out.append(table(d, ["block", "detector"],
                         ["auroc_ood", "auroc_unknown_vs_benign", "unknown_recall", "benign_rejected_as_unknown",
                          "benign_false_alarm_rate"] + rc))

    for det, pat in (("MLP 2k", "mlp2k_{mode}_family_seed{{s}}.csv"), ("Autoencoder", "ae_{mode}_family_seed{{s}}.csv")):
        for mode in ("dedupnone", "dedupmajority"):
            d = load(pat.format(mode=mode))
            if not len(d):
                continue
            d = d[d["calibration"] == "target_warmup_far0.01"]
            if "score" in d and det == "MLP 2k":
                d = d[(d["score"] == "maha") & (d["warmup_contamination"].round(2) == 0)]
            out.append(f"## E8. {det}, de-duplication = {mode} (1% warm-up budget, clean window)\n")
            out.append(table(d, ["protocol"], ["auroc_ood", "auroc_unknown_vs_benign", "unknown_recall",
                                               "benign_false_alarm_rate"]))

    d = load("chrono_family_seed{s}.csv")
    if len(d):
        out.append("## E10. Chronological partitions within each family (P1)\n")
        out.append(table(d, ["detector", "calibration"], ["auroc_ood", "auroc_unknown_vs_benign"] + core))

    d = load("extra_baselines_family_seed{s}.csv")
    if len(d):
        d = d[d["calibration"] == "target_warmup_far0.01"]
        out.append("## E12. Additional baselines (1% warm-up budget, clean window)\n")
        out.append(table(d, ["protocol", "method"], ["auroc_ood", "auroc_unknown_vs_benign", "unknown_recall",
                                                     "benign_false_alarm_rate", "known_macro_f1"]))

    d = load("robust_family_seed{s}.csv")
    if len(d):
        out.append("## E13. Robust window rules under zero-day contamination (RF)\n")
        out.append(table(d, ["protocol", "condition", "calibration"], core))

    for name, pat in (("SecBERT", "l1_secbert-nan_family_seed{s}.csv"), ("RF 2k bin5", "rf_bin5nan_cap2000_family_seed{s}.csv"),
                      ("MLP 2k bin5", "mlp_bin5nan_cap2000_family_seed{s}.csv")):
        d = load(pat)
        if not len(d):
            continue
        d = d[d["calibration"] == "target_warmup_far0.01"]
        if "warmup_contamination" in d:
            d = d[d["warmup_contamination"].round(2) == 0]
        if "score" in d:
            d = d[d["score"] == ("msp" if name.startswith("RF") else "maha")]
        out.append(f"## E14. {name} with an explicit missing-value token (splits with NF-BoT-IoT-v3)\n")
        out.append(table(d, ["protocol"], ["auroc_ood", "unknown_recall", "benign_false_alarm_rate"]))

    text = "\n".join(out)
    (ROOT / "results/revision_summary.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
