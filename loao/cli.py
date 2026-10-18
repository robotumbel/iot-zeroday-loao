"""Command line entry points.

python -m loao.cli prepare --datasets nf_ton_iot_v3 nf_bot_iot_v3 --cap 50000 --seed 0
python -m loao.cli splits  --processed data/processed/*.parquet --protocols P1 P2 P3 --level family --seed 0
"""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

import pandas as pd

from .data import prepare_dataset
from .splits import enumerate_specs, write_manifests
from .taxonomy import Taxonomy

ROOT = Path(__file__).resolve().parent.parent


def cmd_prepare(a: argparse.Namespace) -> None:
    cfgs = json.loads(Path(a.datasets_config).read_text(encoding="utf-8"))
    tax = Taxonomy(a.taxonomy)
    for name in a.datasets:
        path = prepare_dataset(name, cfgs[name], tax, Path(a.root), Path(a.out),
                               a.cap, a.seed, tuple(a.fractions), dedup=a.dedup, time_col=a.time_col, tag=a.tag)
        print(f"[prepare] {name} -> {path}")


def cmd_splits(a: argparse.Namespace) -> None:
    files = [Path(p) for pat in a.processed for p in sorted(glob.glob(pat))]
    if not files:
        raise SystemExit("no processed files found")
    datasets, spaces, paths = {}, {}, {}
    for f in files:
        if f.name.endswith(".time.parquet"):  # timestamp sidecars are not datasets
            continue
        stats = json.loads(f.with_suffix(".stats.json").read_text(encoding="utf-8"))
        name = stats["dataset"]
        datasets[name] = pd.read_parquet(f)
        spaces[name] = stats["feature_space"]
        paths[name] = f
    specs = enumerate_specs(datasets, spaces, a.protocols, a.level, a.seed, a.min_unit_rows,
                            a.include_target_only_unknowns)
    out = Path(a.out) / f"{a.level}_seed{a.seed}"
    index = write_manifests(specs, datasets, paths, out, a.min_unit_rows)
    print(index.groupby(["protocol", "status"]).size().to_string())
    print(f"[splits] {len(index)} manifests -> {out}")


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="loao")
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("prepare", help="load, cap, harmonize, dedup and partition datasets")
    pp.add_argument("--datasets", nargs="+", required=True)
    pp.add_argument("--datasets-config", default=str(ROOT / "configs/datasets.json"))
    pp.add_argument("--taxonomy", default=str(ROOT / "configs/taxonomy.json"))
    pp.add_argument("--root", default=str(ROOT))
    pp.add_argument("--out", default=str(ROOT / "data/processed"))
    pp.add_argument("--cap", type=int, default=50_000, help="max rows per raw label")
    pp.add_argument("--seed", type=int, default=0)
    pp.add_argument("--fractions", type=float, nargs=3, default=[0.6, 0.2, 0.2])
    pp.add_argument("--dedup", default="drop_conflicts", choices=["drop_conflicts", "majority", "none"])
    pp.add_argument("--time-col", default=None, help="raw column saved to a .time.parquet sidecar (not a feature)")
    pp.add_argument("--tag", default="", help="suffix for output file names, e.g. __dedupnone")
    pp.set_defaults(func=cmd_prepare)

    ps = sub.add_parser("splits", help="enumerate protocol splits and write manifests")
    ps.add_argument("--processed", nargs="+", required=True, help="processed parquet files (globs ok)")
    ps.add_argument("--protocols", nargs="+", default=["P1", "P2", "P3"], choices=["P1", "P2", "P3"])
    ps.add_argument("--level", default="family", choices=["family", "subfamily"])
    ps.add_argument("--seed", type=int, default=0)
    ps.add_argument("--min-unit-rows", type=int, default=30)
    ps.add_argument("--include-target-only-unknowns", action="store_true")
    ps.add_argument("--out", default=str(ROOT / "splits"))
    ps.set_defaults(func=cmd_splits)

    a = p.parse_args(argv)
    a.func(a)


if __name__ == "__main__":
    main()
