"""Three-seed summary of the RF threshold-rule analyses (paper Sections VI-A to VI-C).

Inputs: results/rfcal_p1_{level}_seed{s}.csv and results/rfcal_p2p3_{level}_seed{s}.csv
Output: results/rfcal_3seeds_summary.md (mean +/- std over seeds; for averages over splits,
the split average is computed per seed first).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SEEDS = (0, 1, 2)


def load(kind: str) -> pd.DataFrame:
    frames = []
    for level in ("family", "subfamily"):
        for s in SEEDS:
            p = ROOT / f"results/rfcal_{kind}_{level}_seed{s}.csv"
            if p.exists():
                frames.append(pd.read_csv(p).assign(seed_run=s))
    d = pd.concat(frames, ignore_index=True)
    d["src"] = d["source"].str.replace("nf_", "").str.replace("_v3", "").str.replace("_iot", "")
    d["tgt"] = d["target"].str.replace("nf_", "").str.replace("_v3", "").str.replace("_iot", "")
    d["contam"] = d["warmup_contamination"].round(2)
    return d


def ms(series_by_seed: pd.Series) -> str:
    return f"{series_by_seed.mean():.3f} ± {series_by_seed.std(ddof=1):.3f}"


def split_mean(d: pd.DataFrame, by: list[str], metric: str) -> pd.DataFrame:
    """Average over splits within each seed, then mean/std over seeds."""
    per_seed = d.groupby(by + ["seed_run"])[metric].mean()
    g = per_seed.groupby(level=list(range(len(by))))
    return pd.DataFrame({"mean": g.mean(), "std": g.std(ddof=1), "n_seeds": g.size()})


def main() -> None:
    out = ["# RF threshold-rule analyses over seeds 0-2\n"]
    p1 = load("p1")
    yo = p1[(p1["calibration"] == "pseudo_youden")]

    # Table: P1 family level, per held-out family, pseudo-Youden.
    fam = yo[yo["level"] == "family"]
    cols = ["auroc_ood", "unknown_recall", "unknown_flagged_malicious", "benign_false_alarm_rate"]
    t = fam.groupby(["src", "holdout"])[cols].agg(["mean", "std"]).round(3)
    out.append("## P1 family level, pseudo-unknown Youden, per held-out family (mean, std over seeds)\n")
    out.append("```\n" + t.to_string() + "\n```")
    for c in cols:
        out.append(f"- mean over families, {c}: {ms(fam.groupby('seed_run')[c].mean())}")

    sub = yo[yo["level"] == "subfamily"]
    out.append(f"\n- subfamily mean AUROC-OOD: {ms(sub.groupby('seed_run')['auroc_ood'].mean())}")
    for h in ("DOS", "DDOS"):
        r = sub[(sub["src"] == "bot") & (sub["holdout"] == h)].set_index("seed_run")
        out.append(f"- BoT subfamily {h}: AUROC {ms(r['auroc_ood'])}, unknown recall {ms(r['unknown_recall'])}, "
                   f"flagged malicious {ms(r['unknown_flagged_malicious'])}")
    r = fam[(fam["src"] == "ton") & (fam["holdout"] == "RECON")].set_index("seed_run")
    out.append(f"- ToN RECON family: AUROC {ms(r['auroc_ood'])}, flagged malicious {ms(r['unknown_flagged_malicious'])}")

    # Threshold rules in P1 (family).
    rules = p1[(p1["level"] == "family") & p1["calibration"].isin(["pseudo_youden", "benign_far0.01", "benign_far0.05"])]
    out.append("\n## P1 family, threshold rules (split mean per seed, then mean ± std)\n")
    for rule, g in rules.groupby("calibration"):
        out.append(f"- {rule}: benign→unknown {ms(g.groupby('seed_run')['benign_rejected_as_unknown'].mean())}; "
                   f"unknown recall {ms(g.groupby('seed_run')['unknown_recall'].mean())}; "
                   f"benign→known attack {ms(g.groupby('seed_run')['benign_as_known_attack'].mean())}; "
                   f"known macro-F1 {ms(g.groupby('seed_run')['known_macro_f1'].mean())}")

    # P2 / P3.
    pp = load("p2p3")
    none = pp[pp["norm"] == "none"]
    out.append("\n## P2 (family, norm none)\n")
    p2 = none[(none["protocol"] == "P2") & (none["level"] == "family")]
    for (src, rule), g in p2[p2["contam"] == 0.05].groupby(["src", "calibration"]):
        r = g.set_index("seed_run")
        out.append(f"- {src}→{'ton' if src == 'bot' else 'bot'} {rule}: benign→unknown {ms(r['benign_rejected_as_unknown'])}, "
                   f"benign→known {ms(r['benign_as_known_attack'])}, known macro-F1 {ms(r['known_macro_f1'])}")

    out.append("\n## P3 AUROC-OOD (norm none), mean over splits\n")
    for level in ("family", "subfamily"):
        g = none[(none["protocol"] == "P3") & (none["level"] == level)].drop_duplicates(["split_id", "seed_run"])
        out.append(f"- {level}: {ms(g.groupby('seed_run')['auroc_ood'].mean())}")
        gn = pp[(pp["norm"] == "per_network") & (pp["protocol"] == "P3") & (pp["level"] == level)
                & (pp["contam"] == 0.05)].drop_duplicates(["split_id", "seed_run"])
        out.append(f"  - with per-network rank normalisation: {ms(gn.groupby('seed_run')['auroc_ood'].mean())}")
    inv = none[(none["protocol"] == "P3") & (none["level"] == "family") & (none["src"] == "ton")
               & (none["holdout"] == "RECON")].drop_duplicates("seed_run").set_index("seed_run")
    out.append(f"- ToN→BoT RECON (family): AUROC {ms(inv['auroc_ood'])}")

    out.append("\n## Threshold rules across networks (family, norm none, contamination 0.05)\n")
    sel = none[(none["level"] == "family") & (none["contam"] == 0.05)]
    t = []
    for (prot, rule), g in sel.groupby(["protocol", "calibration"]):
        row = {"protocol": prot, "rule": rule}
        for c in ("auroc_ood", "unknown_recall", "benign_rejected_as_unknown", "benign_as_known_attack"):
            ps = g.groupby("seed_run")[c].mean()
            row[c] = f"{ps.mean():.3f} ± {ps.std(ddof=1):.3f}"
        t.append(row)
    out.append("```\n" + pd.DataFrame(t).to_string(index=False) + "\n```")

    out.append("\n## Ranges used in the text\n")
    w = pp[pp["calibration"].str.startswith("target_warmup")]
    for rule in ("target_warmup_far0.01", "target_warmup_far0.05"):
        g = w[(w["calibration"] == rule) & (w["contam"] == 0.05)]
        means = g.groupby(["protocol", "level", "norm", "seed_run"])["benign_rejected_as_unknown"].mean() \
            .groupby(level=[0, 1, 2]).mean()
        out.append(f"- {rule}, contamination 0.05, benign→unknown over protocol × level × norm: "
                   f"{means.min():.3f}–{means.max():.3f}")
    g = w[(w["calibration"] == "target_warmup_far0.01") & (w["contam"] == 0.2)]
    means = g.groupby(["protocol", "level", "norm", "seed_run"])["benign_rejected_as_unknown"].mean() \
        .groupby(level=[0, 1, 2]).mean()
    out.append(f"- target_warmup_far0.01, contamination 0.20, benign→unknown: max {means.max():.3f}")
    src_rules = pp[(pp["calibration"] == "benign_far0.01") & (pp["contam"] == 0.05) & (pp["norm"] == "none")]
    means = src_rules.groupby(["protocol", "level", "seed_run"])["benign_rejected_as_unknown"].mean() \
        .groupby(level=[0, 1]).mean()
    out.append(f"- source benign_far0.01, benign→unknown over protocol × level: {means.min():.3f}–{means.max():.3f}")
    for norm in ("none", "per_network"):
        g = w[(w["protocol"] == "P3") & (w["norm"] == norm) & (w["contam"] == 0.05)]
        means = g.groupby(["level", "calibration", "seed_run"])["unknown_recall"].mean().groupby(level=[0, 1]).mean()
        out.append(f"- P3 warm-up unknown recall ({norm}): {means.min():.3f}–{means.max():.3f}")
    g = pp[(pp["protocol"] == "P3") & (pp["norm"] == "none") & (pp["contam"] == 0.05)
           & pp["calibration"].isin(["pseudo_youden", "benign_far0.01", "benign_far0.05"])]
    rec = g.groupby(["level", "calibration", "seed_run"])["unknown_recall"].mean().groupby(level=[0, 1]).mean()
    rej = g.groupby(["level", "calibration", "seed_run"])["benign_rejected_as_unknown"].mean().groupby(level=[0, 1]).mean()
    out.append(f"- P3 source-calibrated unknown recall: {rec.min():.3f}–{rec.max():.3f}; "
               f"benign→unknown {rej.min():.3f}–{rej.max():.3f}")
    gk = pp[(pp["protocol"] == "P2") & (pp["norm"] == "none") & (pp["contam"] == 0.05)]
    kf = gk.groupby(["level", "calibration", "seed_run"])["known_macro_f1"].mean().groupby(level=[0, 1]).mean()
    out.append(f"- P2 known macro-F1: {kf.min():.3f}–{kf.max():.3f}")
    gb = w[(w["contam"] == 0.05)]
    ba = gb.groupby(["protocol", "level", "norm", "seed_run"])["benign_as_known_attack"].mean().groupby(level=[0, 1, 2]).mean()
    out.append(f"- benign→known attack under warm-up rules: {ba.min():.3f}–{ba.max():.3f}")

    text = "\n".join(out) + "\n"
    (ROOT / "results/rfcal_3seeds_summary.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
