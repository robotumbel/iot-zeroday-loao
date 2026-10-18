"""Unsupervised adaptation to a new network using a short unlabeled warm-up window.

Deployment scenario: the detector is trained on network A and installed on network B.
During a warm-up period, B's traffic is recorded without labels. It is mostly benign
but may contain some attacks (contamination), possibly including the zero-day itself.

make_warmup        simulates that window from the target pool. Labels are used only to
                   control and report the contamination; methods must not read them.
NetworkNormalizer  per-network rank (quantile) transform fitted on one network's own
                   warm-up traffic, so each network is expressed relative to its normal profile.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import QuantileTransformer

from .data import feature_columns
from .taxonomy import BENIGN


def make_warmup(pool: pd.DataFrame, unit_col: str, n: int, contamination: float, seed: int,
                attack_source: str = "all", holdout: str | None = None) -> tuple[pd.DataFrame, dict]:
    """attack_source: 'all' (any target unit), 'known' (units other than the held-out one), or
    'holdout' (the held-out unit only) -- separates zero-day from known-attack contamination."""
    if not 0.0 <= contamination < 1.0:
        raise ValueError("contamination must be in [0, 1)")
    rng = np.random.default_rng(seed)
    benign = pool[pool[unit_col] == BENIGN]
    attacks = pool[pool[unit_col] != BENIGN]
    if attack_source == "known":
        attacks = attacks[attacks[unit_col] != holdout]
    elif attack_source == "holdout":
        attacks = attacks[attacks[unit_col] == holdout]
    elif attack_source != "all":
        raise ValueError("attack_source must be 'all', 'known' or 'holdout'")
    # Keep the requested contamination exact; shrink the window if benign flows run short.
    n_ben = min(n - int(round(n * contamination)), len(benign))
    n_att = min(int(round(n_ben * contamination / (1.0 - contamination))), len(attacks))
    take_b = benign.iloc[rng.choice(len(benign), n_ben, replace=False)] if n_ben else benign.iloc[:0]
    take_a = attacks.iloc[rng.choice(len(attacks), n_att, replace=False)] if n_att else attacks.iloc[:0]
    w = pd.concat([take_b, take_a]).sample(frac=1.0, random_state=seed)
    info = {
        "warmup_requested": n,
        "warmup_size": int(len(w)),
        "warmup_contamination": float(n_att / max(len(w), 1)),
        "warmup_attack_units": take_a[unit_col].value_counts().to_dict(),
        "warmup_attack_source": attack_source,
        "warmup_holdout_share": float((take_a[unit_col] == holdout).sum() / max(len(w), 1)) if holdout else 0.0,
    }
    return w, info


class NetworkNormalizer:
    """Per-feature rank transform to [0, 1], fitted on one network's (unlabeled) traffic. NaN stays NaN."""

    def __init__(self, n_quantiles: int = 1000, seed: int = 0):
        self.n_quantiles = n_quantiles
        self.seed = seed
        self.features: list[str] = []
        self.qt: QuantileTransformer | None = None

    def fit(self, df: pd.DataFrame) -> "NetworkNormalizer":
        self.features = [c for c in feature_columns(df) if pd.api.types.is_numeric_dtype(df[c])]
        X = df[self.features].to_numpy(dtype=float)
        self.qt = QuantileTransformer(n_quantiles=min(self.n_quantiles, len(X)),
                                      output_distribution="uniform", random_state=self.seed)
        self.qt.fit(X)
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.qt is None:
            raise RuntimeError("fit() first")
        out = df.copy()
        out[self.features] = self.qt.transform(df[self.features].to_numpy(dtype=float))
        return out
