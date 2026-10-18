#!/usr/bin/env bash
# Runs every neural detector on the family-level P1/P3 splits for seeds 0-2.
# Waits for each seed's split index (created by `loao.cli splits`). Safe to restart: finished splits are skipped.
set -u
cd "$(dirname "$0")/.."
for s in 0 1 2; do
  until [ -f "splits/family_seed$s/index.csv" ]; do sleep 30; done
  S="--splits splits/family_seed$s --only P1__ P3__ --seed $s"
  python scripts/run_neural.py $S --model mlp --epochs 30 --lr 1e-3 --max-train-per-unit 2000 --out results/mlp_cap2000_family_seed$s.csv > results/mlp_cap2000_seed$s.log 2>&1
  python scripts/run_neural.py $S --model mlp --epochs 30 --lr 1e-3 --max-train-per-unit 0 --out results/mlp_full_family_seed$s.csv > results/mlp_full_seed$s.log 2>&1
  python scripts/run_neural.py $S --model tiny-local --scheme sentence --epochs 3 --batch-size 64 --lr 3e-4 --out results/l1_tiny-local_family_seed$s.csv > results/l1_tiny-local_seed$s.log 2>&1
  for M in distilbert secbert; do
    python scripts/run_neural.py $S --model $M --scheme sentence --out results/l1_${M}_family_seed$s.csv > results/l1_${M}_seed$s.log 2>&1
  done
done
echo ALL_DONE
