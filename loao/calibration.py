"""Threshold rules for the unknown score, using source-domain data only.

Every rule returns a Threshold; a flow is flagged UNKNOWN when `flags(score)` is true.

pseudo_youden : nested pseudo-unknown folds, Youden-J point per fold, thresholds averaged.
benign_far    : fixed false-alarm budget on benign validation flows (e.g. 1% or 5%).
target_warmup_far : the same budget on an unlabeled warm-up window from the target network.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import roc_curve


@dataclass(frozen=True)
class Threshold:
    rule: str
    value: float
    strict: bool  # True: flag if score > value; False: flag if score >= value

    def flags(self, score: np.ndarray) -> np.ndarray:
        s = np.asarray(score, dtype=float)
        return s > self.value if self.strict else s >= self.value


def youden(y_unknown: np.ndarray, score: np.ndarray) -> float:
    fpr, tpr, thr = roc_curve(y_unknown, score)
    return float(thr[np.argmax(tpr - fpr)])


def pseudo_youden(fold_scores: list[tuple[np.ndarray, np.ndarray]]) -> Threshold:
    """fold_scores: per pseudo-unknown fold, (scores of in-distribution flows, scores of pseudo-unknown flows)."""
    if not fold_scores:
        raise ValueError("no pseudo-unknown folds available")
    ths = []
    for s_in, s_out in fold_scores:
        y = np.r_[np.zeros(len(s_in)), np.ones(len(s_out))]
        ths.append(youden(y, np.r_[s_in, s_out]))
    return Threshold("pseudo_youden", float(np.mean(ths)), strict=False)


def benign_far(benign_val_scores: np.ndarray, far: float) -> Threshold:
    """Smallest threshold t with share(benign score > t) <= far.

    Using a strict comparison keeps the budget even when many scores tie (e.g. MSP = 0).
    """
    s = np.sort(np.asarray(benign_val_scores, dtype=float))
    if len(s) == 0:
        raise ValueError("no benign validation flows")
    k = int(np.ceil((1.0 - far) * len(s))) - 1
    t = float(s[min(max(k, 0), len(s) - 1)])
    return Threshold(f"benign_far{far:g}", t, strict=True)


def target_warmup_far(warmup_scores: np.ndarray, far: float) -> Threshold:
    """Same budget rule, applied to an UNLABELED warm-up window from the target network.

    The window is treated as if it were benign; attacks inside it only make the rule
    more conservative (they sit in the top tail and absorb part of the budget).
    """
    th = benign_far(warmup_scores, far)
    return Threshold(f"target_warmup_far{far:g}", th.value, th.strict)
