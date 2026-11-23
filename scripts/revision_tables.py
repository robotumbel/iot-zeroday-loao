"""Tables requested in the first-round review (IEEE Access, Nov 2026). Writes results/revision_tables.md.

A. Standard metrics per detector (pre-specified score, 1% warm-up budget, clean window), P1 and P3:
   detection rate (held-out flows raised as any attack), unknown recall, unknown precision,
   unknown F1, AUPRC, FPR at 95% unknown recall, false-positive rate (total benign alert rate),
   known-attack macro-F1.
B. Per-family P1 AUROC-OOD for every detector.
C. Per-split P3 AUROC-OOD and unknown recall for every detector.
D. Flows per family before and after removal of conflicting feature vectors (seeds 0-2).
E. Training flows per detector and split.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import aggregate_tierb  # noqa: E402
import stats_tests  # noqa: E402

RULE = "target_warmup_far0.01"
ROWS = [("RF full", "msp"), ("RF 2k", "msp"), ("RF 2k bin5", "msp"), ("LightGBM", "native"),
        ("MLP full", "maha"), ("MLP 2k", "maha"), ("MLP 2k bin5", "maha"),
        ("Isolation Forest", "native"), ("Autoencoder", "native"),
        ("tiny-local", "maha"), ("DistilBERT", "maha"), ("SecBERT", "maha"), ("SecBERT-kv", "maha")]
SHORT = {"P1|ton>ton": "ToN", "P1|bot>bot": "BoT"}


def load_all() -> pd.DataFrame:
    d = stats_tests.load(RULE, 0.0, [0, 1, 2])
    a = aggregate_tierb.load("results/anomaly_family_seed{s}.csv")
    a = a[(a["calibration"] == RULE) & (a["warmup_contamination"].round(2) == 0)].copy()
    a["method"] = a["method"].map({"iforest": "Isolation Forest", "ae": "Autoencoder", "lightgbm": "LightGBM"})
    a["score"] = "native"
    a["block"] = a["protocol"] + "|" + a["source"].str[3:6] + ">" + a["target"].str[3:6] + "|" + a["holdout"].astype(str)
    d = pd.concat([d, a], ignore_index=True)
    keep = pd.Series(False, index=d.index)
    for m, s in ROWS:
        keep |= (d["method"] == m) & (d["score"] == s)
    d = d[keep].copy()
    p, r = d["unknown_precision"].fillna(0), d["unknown_recall"].fillna(0)
    d["unknown_f1"] = np.where(p + r > 0, 2 * p * r / (p + r).replace(0, 1), 0.0)
    return d


def ms(g: pd.DataFrame, col: str, digits: int = 3) -> str:
    s = g.groupby("seed_run")[col].mean()
    if len(s) == 0 or s.isna().all():
        return "-"
    return f"{s.mean():.{digits}f} ± {s.std(ddof=1):.{digits}f}" if len(s) > 1 else f"{s.mean():.{digits}f}"


def table_a(d: pd.DataFrame) -> str:
    cols = [("unknown_flagged_malicious", "DetRate"), ("unknown_recall", "UnkRec"), ("unknown_precision", "UnkPrec"),
            ("unknown_f1", "UnkF1"), ("aupr_unknown", "AUPRC"), ("fpr_at_95tpr", "FPR@95"),
            ("benign_false_alarm_rate", "FPR(benign alerts)"), ("known_macro_f1", "KnownMacroF1")]
    out = []
    for prot in ("P1", "P3"):
        rows = []
        for m, s in ROWS:
            g = d[(d["method"] == m) & (d["protocol"] == prot)]
            rows.append({"detector": m, "score": s, **{lab: ms(g, c) for c, lab in cols}})
        out.append(f"### {prot}\n\n```\n{pd.DataFrame(rows).to_string(index=False)}\n```\n")
    return "\n".join(out)


def table_b(d: pd.DataFrame) -> str:
    g = d[d["protocol"] == "P1"].groupby(["block", "method", "seed_run"])["auroc_ood"].mean()
    g = g.groupby(["block", "method"]).mean().unstack()
    g = g[[m for m, _ in ROWS if m in g.columns]]
    g.index = [b.split("|")[1][:3].upper().replace("TON", "ToN").replace("BOT", "BoT") + " " + b.split("|")[2]
               for b in g.index]
    return "```\n" + g.round(3).to_string() + "\n```\n"


def table_c(d: pd.DataFrame) -> str:
    out = []
    for col in ("auroc_ood", "unknown_recall"):
        g = d[d["protocol"] == "P3"].groupby(["block", "method", "seed_run"])[col].mean()
        g = g.groupby(["block", "method"]).mean().unstack()
        g = g[[m for m, _ in ROWS if m in g.columns]]
        out.append(f"{col}:\n```\n" + g.round(3).to_string() + "\n```\n")
    return "\n".join(out)


def table_d() -> str:
    rows = []
    for ds in ("nf_ton_iot_v3", "nf_bot_iot_v3"):
        for s in (0, 1, 2):
            raw = pd.read_parquet(ROOT / f"data/processed/{ds}__cap20000__seed{s}__dedupnone.parquet", columns=["family"])
            kept = pd.read_parquet(ROOT / f"data/processed/{ds}__cap20000__seed{s}.parquet", columns=["family"])
            a, b = raw["family"].value_counts(), kept["family"].value_counts()
            for f in a.index:
                rows.append({"dataset": ds, "seed": s, "family": f, "sampled": int(a[f]), "kept": int(b.get(f, 0))})
    t = pd.DataFrame(rows).groupby(["dataset", "family"])[["sampled", "kept"]].mean().round(0)
    t["kept_share"] = (t["kept"] / t["sampled"]).round(3)
    return "Mean over seeds 0-2; 'sampled' = after the 20k cap, before any de-duplication.\n\n```\n" + t.to_string() + "\n```\n"


def table_e(d: pd.DataFrame) -> str:
    if "n_train" not in d:
        return "n_train not recorded\n"
    g = d[d["protocol"] == "P1"].groupby("method")["n_train"].agg(["min", "median", "max"]).round(0)
    return "P1, flows used for training per split (min / median / max over splits and seeds):\n\n```\n" + g.to_string() + "\n```\n"


def main() -> None:
    d = load_all()
    text = ["# Tables for the first-round revision\n",
            "## A. Standard metrics (1% warm-up budget, clean window; mean ± sd over seeds)\n",
            "DetRate: held-out flows raised as any non-benign label. UnkRec/UnkPrec/UnkF1: the held-out unit as the"
            " positive class of the UNKNOWN decision. FPR(benign alerts): benign flows raised as unknown or as a known"
            " attack.\n", table_a(d),
            "## B. P1 AUROC-OOD per held-out family\n", table_b(d),
            "## C. P3 per split\n", table_c(d),
            "## D. Flows per family before and after removal of conflicting vectors\n", table_d(),
            "## E. Training-set sizes\n", table_e(d)]
    s = "\n".join(text)
    (ROOT / "results/revision_tables.md").write_text(s, encoding="utf-8")
    print(s)


if __name__ == "__main__":
    main()
