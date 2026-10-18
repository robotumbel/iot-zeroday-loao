"""Flow-to-text serialization schemes for language models (RQ4 ablation).

kv        "IN_BYTES=1520 OUT_BYTES=0 PROTOCOL=6 ..."
binned    "IN_BYTES=q7 OUT_BYTES=q0 PROTOCOL=6 ..."   (quantile bins fitted on training data)
sentence  "in bytes is high, out bytes is very low, protocol is 6, ..."
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SCHEMES = ("kv", "binned", "sentence")
_LEVEL_WORDS = ["very low", "low", "medium", "high", "very high"]


class FlowSerializer:
    def __init__(self, scheme: str = "kv", n_bins: int = 10, decimals: int = 4,
                 categorical: list[str] | None = None, max_unique_numeric_as_cat: int = 16):
        if scheme not in SCHEMES:
            raise ValueError(f"scheme must be one of {SCHEMES}")
        self.scheme = scheme
        self.n_bins = n_bins if scheme == "binned" else len(_LEVEL_WORDS)
        self.decimals = decimals
        self.categorical = set(categorical or [])
        self.max_unique = max_unique_numeric_as_cat
        self.edges: dict[str, np.ndarray] = {}
        self.columns: list[str] = []

    def fit(self, df: pd.DataFrame) -> "FlowSerializer":
        self.columns = list(df.columns)
        for c in self.columns:
            col = df[c]
            if c in self.categorical or not pd.api.types.is_numeric_dtype(col) or col.nunique() <= self.max_unique:
                self.categorical.add(c)
                continue
            qs = np.unique(np.nanquantile(col.to_numpy(dtype=float), np.linspace(0, 1, self.n_bins + 1)[1:-1]))
            self.edges[c] = qs
        return self

    def _fmt_raw(self, v) -> str:
        if isinstance(v, (float, np.floating)):
            if np.isnan(v):
                return "nan"
            return f"{v:.{self.decimals}g}"
        return str(v)

    def transform(self, df: pd.DataFrame) -> list[str]:
        if list(df.columns) != self.columns:
            raise ValueError("columns differ from those seen in fit()")
        parts = []
        for c in self.columns:
            vals = df[c].to_numpy()
            if self.scheme == "kv" or c in self.categorical:
                tok = [self._fmt_raw(v) for v in vals]
            else:
                b = np.searchsorted(self.edges[c], vals.astype(float), side="right")
                tok = [f"q{i}" for i in b] if self.scheme == "binned" else [_LEVEL_WORDS[min(i, 4)] for i in b]
            if self.scheme == "sentence":
                name = c.lower().replace("_", " ").replace(".", " ")
                parts.append([f"{name} is {t}" for t in tok])
            else:
                parts.append([f"{c}={t}" for t in tok])
        sep = ", " if self.scheme == "sentence" else " "
        return [sep.join(row) for row in zip(*parts)]


class Discretizer:
    """Numeric twin of the `sentence` / `binned` text schemes, for control experiments.

    Columns treated as categorical by FlowSerializer keep their raw value; every other column
    is replaced by its quantile-bin index (0 .. n_bins-1), with the same edges the
    text serialization uses. RF or MLP trained on this output sees exactly the information the
    language encoders see.
    """

    def __init__(self, n_bins: int = 5):
        self.ser = FlowSerializer("sentence" if n_bins == len(_LEVEL_WORDS) else "binned", n_bins=n_bins)

    def fit(self, df: pd.DataFrame) -> "Discretizer":
        self.ser.fit(df)
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        for c in self.ser.columns:
            if c in self.ser.categorical:
                continue
            v = df[c].to_numpy(dtype=float)
            # Same mapping as the text scheme, including NaN (which the text scheme puts in the top bin).
            out[c] = np.minimum(np.searchsorted(self.ser.edges[c], v, side="right"), self.ser.n_bins - 1).astype(float)
        return out
