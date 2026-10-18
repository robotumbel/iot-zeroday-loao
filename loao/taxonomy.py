"""Harmonized attack taxonomy shared by all datasets."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

BENIGN = "BENIGN"
LEVELS = ("family", "subfamily")


def normalize_label(raw: str) -> str:
    """Lowercase and keep only [a-z0-9], so 'DDoS-ICMP_Flood' and 'ddos icmp flood' match."""
    return re.sub(r"[^a-z0-9]", "", str(raw).strip().lower())


class Taxonomy:
    def __init__(self, path: str | Path):
        spec = json.loads(Path(path).read_text(encoding="utf-8"))
        self.families: list[str] = spec["families"]
        self.mappings: dict[str, dict[str, tuple[str, str]]] = {
            name: {k: tuple(v) for k, v in table.items()}
            for name, table in spec["datasets"].items()
        }
        for name, table in self.mappings.items():
            for raw, (fam, _) in table.items():
                if fam not in self.families:
                    raise ValueError(f"{name}:{raw} maps to unknown family {fam!r}")

    def map_labels(self, labels: pd.Series, taxonomy_name: str) -> pd.DataFrame:
        """Return a frame with columns family, subfamily. Raises on any unmapped label."""
        table = self.mappings[taxonomy_name]
        norm = labels.map(normalize_label)
        unmapped = sorted(set(norm.unique()) - set(table))
        if unmapped:
            raw_examples = labels[norm.isin(unmapped)].drop_duplicates().tolist()[:20]
            raise KeyError(
                f"Unmapped labels for taxonomy {taxonomy_name!r}: {raw_examples}. "
                "Add them to configs/taxonomy.json."
            )
        fam = norm.map(lambda k: table[k][0])
        sub = norm.map(lambda k: table[k][1])
        return pd.DataFrame({"family": fam, "subfamily": sub}, index=labels.index)
