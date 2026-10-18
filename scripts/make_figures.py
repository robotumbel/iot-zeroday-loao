"""Publication figures for the manuscript (vector PDF, print- and grayscale-friendly).

Writes paper/figs/fig{1..5}_*.pdf from the three-seed result files.
Palette: reference categorical slots 1-3 (blue, orange, aqua), validated all-pairs for
colour-vision deficiency; identity is also carried by markers, hatches and direct labels.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402
from scipy.stats import studentized_range  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import aggregate_rfcal  # noqa: E402
import aggregate_tierb  # noqa: E402
import stats_tests  # noqa: E402

OUT = ROOT / "paper" / "figs"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
COL, FULL = 3.5, 7.16  # IEEE column and page widths (inches)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7.5, "axes.titlesize": 8, "axes.labelsize": 7.5,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7, "axes.edgecolor": MUTED,
    "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "axes.linewidth": 0.6,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6, "axes.spines.top": False,
    "axes.spines.right": False, "pdf.fonttype": 42, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})


def grid(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)


# ---------------------------------------------------------------- Fig. 1: protocols
def fig_protocols() -> None:
    fig, ax = plt.subplots(figsize=(FULL, 2.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 44)
    ax.axis("off")

    def box(x, y, w, h, text, fc="#f3f2ee", ec=MUTED):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=0.8", fc=fc, ec=ec, lw=0.7))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=6.6, color=INK, linespacing=1.2)

    def arrow(x0, y0, x1, y1, color=INK2):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=7, color=color, lw=0.8))

    rows = [
        ("P1  within network", "Network A train/val\nunit k removed", "Network A test\nbenign + known + k",
         "k = unknown"),
        ("P2  closed-set transfer", "Network A train/val\nall units", "Network B test\nbenign + units known in A",
         "no unknown"),
        ("P3  cross-network LOAO", "Network A train/val\nunit k removed", "Network B test\nbenign + known + k",
         "k = unknown"),
    ]
    ys = [30.5, 17.5, 4.5]
    for (name, train, test, note), y in zip(rows, ys):
        ax.text(1, y + 8.3, name, ha="left", va="center", fontsize=7.2, fontweight="bold", color=INK)
        box(1, y, 19, 6.6, train, fc="#eaf1fb", ec=BLUE)
        box(25, y, 15, 6.6, "Detector\nnovelty score s(x)", fc="#ffffff")
        box(45.5, y, 22, 6.6, test, fc="#fdeee7", ec=ORANGE)
        ax.text(68.4, y + 1.4, note, ha="left", va="center", fontsize=6.4, color=INK2, style="italic")
        arrow(20.3, y + 3.3, 24.7, y + 3.3)
        arrow(40.3, y + 3.3, 45.2, y + 3.3)
    box(81.5, 11, 17.5, 18, "Unlabeled warm-up\nwindow from\nnetwork B\n\nthreshold $\\tau_W$:\nat most $\\alpha$ of the\nwindow above it",
        fc="#e8f6f0", ec=AQUA)
    arrow(81.3, 21.5, 67.8, 22.6, color=AQUA)
    arrow(81.3, 17.0, 67.8, 9.6, color=AQUA)
    ax.text(99, 42.5, "Units: family (far-OOD) or subfamily (near-OOD, e.g., DoS held out while DDoS is known)",
            ha="right", va="center", fontsize=6.4, color=INK2)
    fig.savefig(OUT / "fig1_protocols.pdf")
    plt.close(fig)


# ---------------------------------------------------------------- Fig. 2: per family
def fig_per_family() -> None:
    p1 = aggregate_rfcal.load("p1")
    d = p1[(p1["level"] == "family") & (p1["calibration"] == "pseudo_youden")]
    g = d.groupby(["src", "holdout"])["auroc_ood"].agg(["mean", "std"]).reset_index()
    g = g.sort_values("mean")
    labels = [f"{h.replace('_', '/')} ({'ToN' if s == 'ton' else 'BoT'})" for s, h in zip(g["src"], g["holdout"])]
    colors = [BLUE if s == "ton" else ORANGE for s in g["src"]]
    hatches = ["" if s == "ton" else "////" for s in g["src"]]
    fig, ax = plt.subplots(figsize=(COL, 2.5))
    y = np.arange(len(g))
    bars = ax.barh(y, g["mean"], xerr=g["std"], height=0.62, color=colors, edgecolor="#fcfcfb", linewidth=0.8,
                   error_kw={"elinewidth": 0.7, "ecolor": INK2, "capsize": 1.5})
    for b, h in zip(bars, hatches):
        b.set_hatch(h)
    for yi, m in zip(y, g["mean"]):
        ax.text(min(m + 0.02, 1.0), yi, f"{m:.2f}", va="center", ha="left", fontsize=6.4, color=INK)
    ax.axvline(0.5, color=MUTED, lw=0.7, ls="--")
    ax.text(0.505, len(g) - 0.4, "chance", fontsize=6.2, color=INK2, va="center")
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 1.08)
    ax.set_xlabel("AUROC-OOD (held-out family vs. all other test flows)")
    grid(ax, "x")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=BLUE, label="NF-ToN-IoT-v3"), Patch(fc=ORANGE, hatch="////", label="NF-BoT-IoT-v3")],
              loc="lower right", frameon=False)
    fig.savefig(OUT / "fig2_per_family.pdf")
    plt.close(fig)


# ---------------------------------------------------------------- Fig. 3: calibration
def fig_calibration() -> None:
    pp = aggregate_rfcal.load("p2p3")
    d = pp[(pp["level"] == "family") & (pp["norm"] == "none") & (pp["contam"] == 0.05)]
    groups = [("P2", "1%"), ("P2", "5%"), ("P3", "1%"), ("P3", "5%")]
    rules = {"source": "benign_far0.0", "warm-up": "target_warmup_far0.0"}
    vals = {k: [] for k in rules}
    for prot, b in groups:
        for k, prefix in rules.items():
            rule = prefix + ("1" if b == "1%" else "5")
            s = d[(d["protocol"] == prot) & (d["calibration"] == rule)].groupby("seed_run")[
                "benign_rejected_as_unknown"].mean() * 100
            vals[k].append((s.mean(), s.std(ddof=1)))
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(FULL, 2.2), gridspec_kw={"width_ratios": [1.15, 1]})
    x = np.arange(len(groups))
    w = 0.36
    for i, (k, color, hatch) in enumerate([("source", BLUE, ""), ("warm-up", AQUA, "////")]):
        m = [v[0] for v in vals[k]]
        e = [v[1] for v in vals[k]]
        bars = ax.bar(x + (i - 0.5) * (w + 0.02), m, w, yerr=e, color=color, hatch=hatch, edgecolor="#fcfcfb",
                      linewidth=0.8, label=f"{k} calibrated",
                      error_kw={"elinewidth": 0.7, "ecolor": INK2, "capsize": 1.5})
        for bx, mv, ev in zip(bars, m, e):
            ax.text(bx.get_x() + bx.get_width() / 2, mv + ev + 2.0, f"{mv:.1f}", ha="center", fontsize=6.2, color=INK)
    for xi, (_, b) in zip(x, groups):
        ax.hlines(1 if b == "1%" else 5, xi - 0.42, xi + 0.42, color=INK, lw=0.9, ls=":")
    ax.set_xticks(x, [f"{p}\nbudget {b}" for p, b in groups])
    ax.set_ylabel("Target benign flows rejected\nas unknown (%)")
    ax.set_ylim(0, 112)
    grid(ax)
    ax.legend(loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.0))
    ax.set_title("Source vs. warm-up thresholds (RF)", fontsize=7.5, color=INK)

    # Right: unknown recall (P1, 1% budget) by what contaminates the window.
    w_ = aggregate_tierb.load("results/rf_windows_family_seed{s}.csv")
    w_ = w_[(w_["protocol"] == "P1") & (w_["calibration"] == "target_warmup_far0.01") & (w_["warmup_requested"] == 2000)]
    base = aggregate_tierb.load("results/rf_msp_full_family_seed{s}.csv")
    base = base[(base["protocol"] == "P1") & (base["calibration"] == "target_warmup_far0.01")
                & (base["warmup_contamination"].round(2) == 0)]
    cats = [("clean", base)]
    for src, lab in (("known", "known\nattacks"), ("holdout", "zero-day\nfamily")):
        for c in (0.05, 0.2):
            g = w_[(w_["warmup_attack_source"] == src) & (w_["warmup_contamination"].round(2) == c)]
            cats.append((f"{lab}\n{int(c * 100)}%", g))
    m = [g.groupby("seed_run")["unknown_recall"].mean() for _, g in cats]
    colors = [MUTED, ORANGE, ORANGE, BLUE, BLUE]
    hatches = ["", "", "", "////", "////"]
    bars = ax2.bar(range(len(cats)), [s.mean() for s in m], 0.62, yerr=[s.std(ddof=1) for s in m], color=colors,
                   edgecolor="#fcfcfb", linewidth=0.8, error_kw={"elinewidth": 0.7, "ecolor": INK2, "capsize": 1.5})
    for b, h, s in zip(bars, hatches, m):
        b.set_hatch(h)
        ax2.text(b.get_x() + b.get_width() / 2, s.mean() + 0.03, f"{s.mean():.2f}", ha="center", fontsize=6.2, color=INK)
    ax2.set_xticks(range(len(cats)), [c for c, _ in cats], fontsize=6.4)
    ax2.set_ylabel("Unknown recall (P1, 1% budget)")
    ax2.set_ylim(0, 0.55)
    grid(ax2)
    ax2.set_title("Window contaminated with ...", fontsize=7.5, color=INK)
    fig.tight_layout(w_pad=2.0)
    fig.savefig(OUT / "fig3_calibration.pdf")
    plt.close(fig)


# ---------------------------------------------------------------- Fig. 4: critical difference
SEL = {
    "RF full|msp": "RF, all data", "RF 2k|msp": "RF, 2k/unit", "RF 2k bin5|msp": "RF, 5 levels",
    "MLP full|maha": "MLP, all data", "MLP 2k|maha": "MLP, 2k/unit", "MLP 2k bin5|maha": "MLP, 5 levels",
    "tiny-local|maha": "Tiny-local", "DistilBERT|maha": "DistilBERT", "SecBERT|maha": "SecBERT",
    "SecBERT-kv|maha": "SecBERT, raw values",
}


def family_of(combo: str) -> str:
    return "RF" if combo.startswith("RF") else ("MLP" if combo.startswith("MLP") else "LM")


FAM_COLOR = {"RF": BLUE, "MLP": ORANGE, "LM": AQUA}
FAM_MARK = {"RF": "s", "MLP": "^", "LM": "o"}


def fig_cd():
    d = stats_tests.load("target_warmup_far0.01", 0.0, [0, 1, 2])
    d = d[(d["protocol"] == "P1") & d["combo"].isin(SEL)]
    m = d.groupby(["block", "combo"])["auroc_ood"].mean().unstack().dropna()
    n, k = m.shape
    ranks = m.rank(axis=1, ascending=False).mean().sort_values()
    cd = studentized_range.ppf(0.95, k, np.inf) / np.sqrt(2) * np.sqrt(k * (k + 1) / (6 * n))
    fig, ax = plt.subplots(figsize=(FULL, 1.9))
    lo, hi = 1, k
    ax.set_xlim(lo - 2.2, hi + 2.2)
    ax.set_ylim(-0.05, 1.42)
    ax.axis("off")
    ax.hlines(1.0, lo, hi, color=INK, lw=0.8)
    for t in range(lo, hi + 1):
        ax.vlines(t, 1.0, 1.04, color=INK, lw=0.8)
        ax.text(t, 1.07, str(t), ha="center", va="bottom", fontsize=6.6, color=INK2)
    ax.text((lo + hi) / 2, 1.36, "Average rank (P1 AUROC-OOD, pre-specified score, 10 splits, 3 seeds; 1 = best)",
            ha="center", fontsize=7, color=INK)
    ax.hlines(1.24, lo, lo + cd, color=INK, lw=1.4)
    ax.text(lo + cd + 0.1, 1.24, f"CD = {cd:.2f}", ha="left", va="center", fontsize=6.6, color=INK)
    items = list(ranks.items())
    half = (len(items) + 1) // 2
    rv = ranks.to_numpy()
    # Cliques: maximal runs of detectors whose rank span is below CD, drawn just under the axis.
    cliques = []
    for i in range(len(rv)):
        j = i
        while j + 1 < len(rv) and rv[j + 1] - rv[i] < cd:
            j += 1
        if j > i and not any(a <= i and j <= b for a, b in cliques):
            cliques.append((i, j))
    for c, (a, b) in enumerate(cliques):
        ax.hlines(0.93 - 0.045 * c, rv[a] - 0.04, rv[b] + 0.04, color=INK2, lw=1.8)
    y0 = 0.93 - 0.045 * max(len(cliques), 1) - 0.06
    for i, (combo, r) in enumerate(items):
        left = i < half
        row = i if left else len(items) - 1 - i
        yline = y0 - row * 0.13
        xtext = lo - 0.3 if left else hi + 0.3
        fam = family_of(combo)
        ax.plot([r, r, xtext], [1.0, yline, yline], color=FAM_COLOR[fam], lw=0.8)
        ax.plot(r, 1.0, marker=FAM_MARK[fam], color=FAM_COLOR[fam], ms=4, mec="#fcfcfb", mew=0.6)
        ax.text(xtext + (-0.08 if left else 0.08), yline, f"{SEL[combo]} ({r:.1f})", ha="right" if left else "left",
                va="center", fontsize=6.4, color=INK)
    fig.savefig(OUT / "fig4_cd.pdf")
    plt.close(fig)
    return n, k, cd


# ---------------------------------------------------------------- Fig. 5: performance vs cost
def fig_cost() -> None:
    t = pd.read_csv(ROOT / "results/paper_table6.csv")
    cost = {"RF full": 0.0086, "LightGBM": 0.011, "MLP full": 0.002, "MLP 2k": 0.002, "Isolation Forest": 0.019,
            "Autoencoder": 0.003, "tiny-local": 0.67, "DistilBERT": 3.6, "SecBERT": 3.0}
    fam = {"RF full": "RF", "LightGBM": "RF", "MLP full": "MLP", "MLP 2k": "MLP", "Isolation Forest": "MLP",
           "Autoencoder": "MLP", "tiny-local": "LM", "DistilBERT": "LM", "SecBERT": "LM"}
    mark = {"RF full": "s", "LightGBM": "D", "MLP full": "^", "MLP 2k": "v", "Isolation Forest": "P",
            "Autoencoder": "X", "tiny-local": "o", "DistilBERT": "h", "SecBERT": "p"}
    t = t[t["detector"].isin(cost)]
    fig, axes = plt.subplots(1, 2, figsize=(FULL, 2.3), sharex=True)
    for ax, col, lab, ylim in zip(axes, ["auroc_unknown_vs_benign|P1", "unknown_recall|P1"],
                                  ["AUROC, zero-day vs. benign (P1)", "Unknown recall at 1% budget (P1)"],
                                  [(0.68, 0.93), (0.0, 0.5)]):
        for _, r in t.iterrows():
            mean, sd = (float(v) for v in str(r[col]).split(" ± ")) if " ± " in str(r[col]) else (float(r[col]), 0.0)
            name = r["detector"]
            ax.errorbar(cost[name], mean, yerr=sd, fmt=mark[name], ms=6, color=FAM_COLOR[fam[name]], mec="#fcfcfb",
                        mew=0.8, elinewidth=0.7, capsize=1.5)
            off = {"MLP full": (6, 5), "MLP 2k": (6, -9), "RF full": (6, -2)}.get(name, (6, 2))
            ax.annotate(name, (cost[name], mean), xytext=off, textcoords="offset points", fontsize=6.0, color=INK)
        ax.set_xscale("log")
        ax.set_xlim(0.001, 40)
        ax.set_ylim(*ylim)
        ax.set_ylabel(lab)
        ax.set_xlabel("Inference time per flow (ms, log scale)")
        grid(ax, "both")
    fig.tight_layout(w_pad=2.0)
    fig.savefig(OUT / "fig5_cost.pdf")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig_protocols()
    fig_calibration()
    n, k, cd = fig_cd()
    fig_cost()
    print(f"figures -> {OUT}; CD figure: {n} splits, {k} combinations, CD = {cd:.2f}")


if __name__ == "__main__":
    main()
