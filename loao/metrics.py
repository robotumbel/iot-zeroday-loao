"""Open-set / zero-day metrics.

Convention: `score` is an unknown-ness score (higher = more likely an unseen attack).
Positives for the threshold-free metrics are flows of the held-out unit.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score, f1_score, roc_auc_score, roc_curve

UNKNOWN = "UNKNOWN"
BENIGN = "BENIGN"


def fpr_at_tpr(y_unknown: np.ndarray, score: np.ndarray, tpr_level: float = 0.95) -> float:
    """Share of non-unknown flows flagged as unknown when `tpr_level` of unknown flows are caught."""
    fpr, tpr, _ = roc_curve(y_unknown, score)
    return float(fpr[np.searchsorted(tpr, tpr_level, side="left")])


def threshold_free(y_unknown, score, is_benign=None) -> dict:
    """With `is_benign`, also report AUROC of the held-out unit against benign flows only, the
    comparison under which benign-only anomaly detectors (which also flag known attacks) are fair."""
    y = np.asarray(y_unknown)
    s = np.asarray(score, dtype=float)
    if y.min() == y.max():
        return {"auroc_ood": np.nan, "aupr_unknown": np.nan, "fpr_at_95tpr": np.nan, "auroc_unknown_vs_benign": np.nan}
    out = {
        "auroc_ood": float(roc_auc_score(y, s)),
        "aupr_unknown": float(average_precision_score(y, s)),
        "fpr_at_95tpr": fpr_at_tpr(y, s, 0.95),
    }
    if is_benign is not None:
        b = np.asarray(is_benign, dtype=bool)
        m = (y == 1) | b
        out["auroc_unknown_vs_benign"] = float(roc_auc_score(y[m], s[m]))
    return out


def open_set_report(true_unit, pred_unit, holdout: str | None) -> dict:
    """Metrics on final open-set predictions.

    true_unit: ground-truth unit per test flow (the held-out unit appears with its own name).
    pred_unit: predicted unit per flow; a known unit, BENIGN, or UNKNOWN.
    """
    t = np.asarray(true_unit, dtype=object)
    p = np.asarray(pred_unit, dtype=object)
    t_open = np.where(t == holdout, UNKNOWN, t) if holdout else t
    is_unk = t_open == UNKNOWN
    is_benign = t_open == BENIGN
    is_known_attack = ~is_unk & ~is_benign
    out = {
        "open_set_macro_f1": float(f1_score(t_open, p, average="macro", zero_division=0)),
        "known_macro_f1": float(f1_score(t_open[~is_unk], p[~is_unk], average="macro", zero_division=0))
        if (~is_unk).any() else np.nan,
        "benign_false_alarm_rate": float((p[is_benign] != BENIGN).mean()) if is_benign.any() else np.nan,
        # Split of the false alarms: threshold-driven vs closed-set confusion.
        "benign_rejected_as_unknown": float((p[is_benign] == UNKNOWN).mean()) if is_benign.any() else np.nan,
        "benign_as_known_attack": float(((p[is_benign] != BENIGN) & (p[is_benign] != UNKNOWN)).mean())
        if is_benign.any() else np.nan,
        "known_attack_rejected_as_unknown": float((p[is_known_attack] == UNKNOWN).mean())
        if is_known_attack.any() else np.nan,
    }
    if is_unk.any():
        out.update({
            "unknown_recall": float((p[is_unk] == UNKNOWN).mean()),
            "unknown_precision": float((t_open[p == UNKNOWN] == UNKNOWN).mean()) if (p == UNKNOWN).any() else 0.0,
            # Practical view: was the zero-day at least raised as malicious (any non-benign label)?
            "unknown_flagged_malicious": float((p[is_unk] != BENIGN).mean()),
        })
    return out
