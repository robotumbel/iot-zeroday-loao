"""Four-network benchmark (E11): NF-ToN-IoT-v3, NF-BoT-IoT-v3, NF-UNSW-NB15-v3, NF-CICIDS2018-v3.

Results for splits that involve only ToN/BoT come from results/ (identical splits); splits that involve
UNSW-NB15 or CIC-IDS2018 come from results/e11/. Each detector uses its pre-specified score, the 1%
warm-up budget and a clean window. Writes results/e11_summary.md with:
  - per-dataset P1 means and the P3 mean over all 24 splits
  - Friedman test + Nemenyi CD over the P1 splits (21) and over the P3 splits (24), detectors present
    on every split only
  - per-pair P3 AUROC
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, studentized_range

ROOT = Path(__file__).resolve().parent.parent
RULE = "target_warmup_far0.01"
# label -> (file stem, score, kind)
DET = {
    "RF full": ("rf_msp_full_family_seed{s}.csv", "msp", "rf"),
    "RF 2k": ("rf_msp_cap2000_family_seed{s}.csv", "msp", "rf"),
    "MLP full": ("mlp_full_family_seed{s}.csv", "maha", "nn"),
    "MLP 2k": ("mlp_cap2000_family_seed{s}.csv", "maha", "nn"),
    "LightGBM": ("anomaly_family_seed{s}.csv", "lightgbm", "anom"),
    "Isolation Forest": ("anomaly_family_seed{s}.csv", "iforest", "anom"),
    "Autoencoder": ("anomaly_family_seed{s}.csv", "ae", "anom"),
    "k-NN raw": ("extra_baselines_family_seed{s}.csv", "knn-raw", "extra"),
    "tiny-local": ("l1_tiny-local_family_seed{s}.csv", "maha", "nn"),
    "DistilBERT": ("l1_distilbert_family_seed{s}.csv", "maha", "nn"),
    "SecBERT": ("l1_secbert_family_seed{s}.csv", "maha", "nn"),
}
OLD_DIR = {"extra": "results/revision"}


def read(label: str, s: int) -> pd.DataFrame:
    stem, sc, kind = DET[label]
    frames = []
    for d in (OLD_DIR.get(kind, "results"), "results/e11"):
        p = ROOT / d / stem.format(s=s)
        if not p.exists():
            continue
        x = pd.read_csv(p)
        if kind == "rf":
            x = x[x.get("norm", "none") == "none"] if "norm" in x else x
        elif kind == "nn":
            x = x[x["score"] == sc]
        elif kind in ("anom", "extra"):
            x = x[x["method"] == sc]
        x = x[x["calibration"] == RULE]
        if "warmup_contamination" in x:
            c = x["warmup_contamination"].round(3)
            x = x[c.isna() | (c == 0)]
        if d == "results/e11":
            x = x[x["split_id"].str.contains("unsw|cicids")]
        else:
            x = x[~x["split_id"].str.contains("unsw|cicids")]
        frames.append(x.drop_duplicates("split_id"))
    if not frames:
        return pd.DataFrame()
    x = pd.concat(frames, ignore_index=True).assign(detector=label, seed_run=s)
    return x


def load() -> pd.DataFrame:
    d = pd.concat([read(l, s) for l in DET for s in (0, 1, 2)], ignore_index=True)
    d["block"] = d["split_id"].str.replace(r"__seed\d+$", "", regex=True)
    d["src"] = d["source"].str.replace("nf_", "").str.replace("_v3", "")
    d["tgt"] = d["target"].str.replace("nf_", "").str.replace("_v3", "")
    return d


def friedman(d: pd.DataFrame, metric: str) -> str:
    m = d.groupby(["block", "detector"])[metric].mean().unstack()
    m = m.dropna(axis=1, thresh=int(0.9 * len(m))).dropna()
    n, k = m.shape
    if n < 3 or k < 3:
        return "too few complete blocks"
    stat, p = friedmanchisquare(*[m[c] for c in m.columns])
    ranks = m.rank(axis=1, ascending=False).mean().sort_values()
    cd = studentized_range.ppf(0.95, k, np.inf) / np.sqrt(2) * np.sqrt(k * (k + 1) / (6 * n))
    return (f"{n} splits, {k} detectors: Friedman chi2 = {stat:.2f}, p = {p:.2e}, Nemenyi CD = {cd:.2f}. "
            "Average ranks: " + ", ".join(f"{i} {v:.2f}" for i, v in ranks.items()))


ORDER = ["RF full", "RF 2k", "LightGBM", "MLP full", "MLP 2k", "k-NN raw", "Isolation Forest", "Autoencoder",
         "tiny-local", "DistilBERT", "SecBERT"]
LABEL = {"RF full": "RF, all data", "RF 2k": "RF, 2k/unit", "MLP full": "MLP, all data", "MLP 2k": "MLP, 2k/unit",
         "k-NN raw": "$k$-NN, raw features", "Isolation Forest": "Isolation Forest", "Autoencoder": "Autoencoder"}


def latex_table(d: pd.DataFrame) -> None:
    """Rows of the four-network table: P1 AUROC-OOD per dataset; P1 recall and alerts over all 21 splits;
    P3 AUROC-OOD, recall and alerts over all 24 splits. A cell needs every split of its column, otherwise
    it is printed as pending."""
    need = d.groupby("protocol")["block"].nunique().to_dict()
    need_src = d[d["protocol"] == "P1"].groupby("src")["block"].nunique().to_dict()

    def cell(g: pd.DataFrame, col: str, n: int, bold: bool = False) -> str:
        if g["block"].nunique() < n:
            return r"\pend"
        s = g.groupby("seed_run")[col].mean()
        return f"{s.mean():.3f}".lstrip("0") + r"$\pm$" + f"{s.std(ddof=1):.3f}".lstrip("0")

    rows = []
    for det in ORDER:
        g = d[d["detector"] == det]
        p1, p3 = g[g["protocol"] == "P1"], g[g["protocol"] == "P3"]
        c = [LABEL.get(det, det)]
        for src in ("ton_iot", "bot_iot", "unsw_nb15", "cicids2018"):
            c.append(cell(p1[p1["src"] == src], "auroc_ood", need_src[src]))
        c += [cell(p1, "unknown_recall", need["P1"]), cell(p1, "benign_false_alarm_rate", need["P1"]),
              cell(p3, "auroc_ood", need["P3"]), cell(p3, "unknown_recall", need["P3"]),
              cell(p3, "benign_false_alarm_rate", need["P3"])]
        rows.append(" & ".join(c) + r" \\")
    out = ROOT / "paper/tables"
    out.mkdir(parents=True, exist_ok=True)
    (out / "four_networks.tex").write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> None:
    d = load()
    cols = ["auroc_ood", "auroc_unknown_vs_benign", "unknown_recall", "benign_false_alarm_rate"]
    out = ["# Four-network benchmark (E11), 1% warm-up budget, clean window\n"]
    p1 = d[d["protocol"] == "P1"]
    t = p1.groupby(["src", "detector", "seed_run"])[cols].mean().groupby(["src", "detector"]).mean().round(3)
    out.append("## P1 per dataset (mean over splits, then over seeds)\n\n```\n" + t.to_string() + "\n```\n")
    t = p1.groupby(["detector", "seed_run"])[cols].mean().groupby("detector").agg(["mean", "std"]).round(3)
    out.append("## P1 all 21 splits\n\n```\n" + t.to_string() + "\n```\n")
    p3 = d[d["protocol"] == "P3"]
    t = p3.groupby(["detector", "seed_run"])[cols].mean().groupby("detector").agg(["mean", "std"]).round(3)
    out.append("## P3 all splits\n\n```\n" + t.to_string() + "\n```\n")
    t = p3.groupby(["src", "tgt", "holdout", "detector"])["auroc_ood"].mean().unstack().round(3)
    out.append("## P3 AUROC-OOD per split\n\n```\n" + t.to_string() + "\n```\n")
    for prot, g in (("P1", p1), ("P3", p3)):
        for metric in ("auroc_ood", "unknown_recall"):
            out.append(f"- {prot} {metric}: " + friedman(g, metric))
    n_blocks = d.groupby("detector")["block"].nunique()
    out.append("\nSplits available per detector: " + ", ".join(f"{k} {v}" for k, v in n_blocks.items()))
    latex_table(d)
    text = "\n".join(out) + "\n"
    (ROOT / "results/e11_summary.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
