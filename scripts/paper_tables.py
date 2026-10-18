"""Numbers for the manuscript's detector-comparison table (Table 6), seeds 0-2.

One row per detector with its pre-specified primary score (Mahalanobis for embedding-based
detectors, MSP for tree ensembles, native score for benign-only detectors), at the 1% warm-up
budget with a clean window. Each cell: mean over splits per seed, then mean ± std over seeds.
SecBERT with raw-value text is included with however many seeds have finished.
Writes results/paper_table6.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import aggregate_tierb  # noqa: E402
import stats_tests  # noqa: E402

ROWS = [("RF full", "msp"), ("RF 2k", "msp"), ("RF 2k bin5", "msp"), ("LightGBM", "native"),
        ("MLP full", "maha"), ("MLP 2k", "maha"), ("MLP 2k bin5", "maha"),
        ("Isolation Forest", "native"), ("Autoencoder", "native"),
        ("tiny-local", "maha"), ("DistilBERT", "maha"), ("SecBERT", "maha"), ("SecBERT-kv", "maha")]
SCORE_DIR = {"MLP full": "MLP_cap0", "MLP 2k": "MLP_cap2000", "MLP 2k bin5": "MLP-bin5_cap2000",
             "tiny-local": "L1-tiny-local_cap2000", "DistilBERT": "L1-distilbert_cap2000",
             "SecBERT": "L1-secbert_cap2000", "SecBERT-kv": "L1-secbert-kv_cap2000"}


def main() -> None:
    d = stats_tests.load("target_warmup_far0.01", 0.0, [0, 1, 2])
    a = aggregate_tierb.load("results/anomaly_family_seed{s}.csv")
    a = a[(a["calibration"] == "target_warmup_far0.01") & (a["warmup_contamination"].round(2) == 0)]
    a["method"] = a["method"].map({"iforest": "Isolation Forest", "ae": "Autoencoder", "lightgbm": "LightGBM"})
    a["score"] = "native"
    nn = aggregate_tierb.neural_auroc_vs_benign()
    rfw = aggregate_tierb.load("results/rf_windows_family_seed{s}.csv").drop_duplicates(["split_id", "seed_run"])
    cols = [("auroc_ood", "P1"), ("auroc_ood", "P3"), ("auroc_unknown_vs_benign", "P1"),
            ("unknown_recall", "P1"), ("unknown_recall", "P3"), ("benign_false_alarm_rate", "P1"),
            ("benign_false_alarm_rate", "P3")]
    out = []
    for meth, sc in ROWS:
        src = a[a["method"] == meth] if sc == "native" else d[(d["method"] == meth) & (d["score"] == sc)]
        row = {"detector": meth, "score": sc, "seeds": int(src["seed_run"].nunique()) if len(src) else 0}
        for metric, prot in cols:
            g = src[src["protocol"] == prot]
            if metric == "auroc_unknown_vs_benign" and sc != "native":
                if meth == "RF full":
                    g = rfw[rfw["protocol"] == prot]
                elif meth in SCORE_DIR:
                    g = nn[(nn["method"] == SCORE_DIR[meth]) & (nn["score"] == sc) & (nn["protocol"] == prot)]
                else:
                    g = g.iloc[0:0]
            if len(g) == 0 or metric not in g:
                row[f"{metric}|{prot}"] = "—"
                continue
            s = g.groupby("seed_run")[metric].mean()
            row[f"{metric}|{prot}"] = f"{s.mean():.3f}" + (f" ± {s.std(ddof=1):.3f}" if len(s) > 1 else "")
        out.append(row)
    t = pd.DataFrame(out)
    text = "# Table 6 numbers (1% warm-up budget, clean window)\n\n```\n" + t.to_string(index=False) + "\n```\n"
    (ROOT / "results/paper_table6.md").write_text(text, encoding="utf-8")
    t.to_csv(ROOT / "results/paper_table6.csv", index=False)
    print(text)


if __name__ == "__main__":
    main()
