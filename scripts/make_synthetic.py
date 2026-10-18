"""Generate small synthetic NetFlow-v3-like datasets to smoke-test the pipeline.

The rows are random Gaussian clusters, NOT real traffic. Label strings follow the real
datasets so the taxonomy mapping is exercised. Writes to data/synthetic/.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES = ["PROTOCOL", "L7_PROTO", "IN_BYTES", "OUT_BYTES", "IN_PKTS", "OUT_PKTS",
            "FLOW_DURATION_MILLISECONDS", "TCP_FLAGS", "MIN_TTL", "MAX_TTL",
            "SRC_TO_DST_AVG_THROUGHPUT", "DST_TO_SRC_AVG_THROUGHPUT", "L4_DST_PORT"]

DATASETS = {
    "NF-ToN-IoT-v3": ["Benign", "scanning", "xss", "injection", "ddos", "dos", "password",
                      "backdoor", "ransomware", "mitm"],
    "NF-BoT-IoT-v3": ["Benign", "Reconnaissance", "DDoS", "DoS", "Theft"],
}


def make(name: str, labels: list[str], n_per_label: int, rng: np.random.Generator, shift: float) -> pd.DataFrame:
    rows = []
    for i, lab in enumerate(labels):
        center = rng.normal(0, 3, len(FEATURES)) + shift
        x = rng.normal(center, 1.0, size=(n_per_label, len(FEATURES)))
        df = pd.DataFrame(np.abs(x) * 100, columns=FEATURES).round(0)
        df["PROTOCOL"] = rng.choice([6, 17, 1], n_per_label)
        df["IPV4_SRC_ADDR"] = [f"192.168.{i}.{j % 255}" for j in range(n_per_label)]
        df["IPV4_DST_ADDR"] = "10.0.0.1"
        df["L4_SRC_PORT"] = rng.integers(1024, 65535, n_per_label)
        df["FLOW_START_MILLISECONDS"] = rng.integers(0, 10**9, n_per_label)
        df["FLOW_END_MILLISECONDS"] = df["FLOW_START_MILLISECONDS"] + 5
        df["Label"] = int(lab.lower() != "benign")
        df["Attack"] = lab
        rows.append(df)
    out = pd.concat(rows, ignore_index=True)
    # Inject duplicates: 20 same-label copies and 10 conflicting-label copies.
    dup = out.sample(20, random_state=1)
    conf = out[out["Attack"] == labels[1]].head(10).copy()
    conf["Attack"] = labels[2]
    return pd.concat([out, dup, conf], ignore_index=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / "data/synthetic"))
    a = ap.parse_args()
    rng = np.random.default_rng(42)
    for k, (name, labels) in enumerate(DATASETS.items()):
        d = Path(a.out) / name
        d.mkdir(parents=True, exist_ok=True)
        df = make(name, labels, a.n, rng, shift=0.5 * k)
        half = len(df) // 2
        df.iloc[:half].to_csv(d / "part1.csv", index=False)
        df.iloc[half:].to_csv(d / "part2.csv", index=False)
        print(f"{name}: {len(df)} rows -> {d}")


if __name__ == "__main__":
    main()
