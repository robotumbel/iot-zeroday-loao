#!/bin/bash
# Revision batch 1 (CPU): LightGBM energy score (E5) and de-duplication sensitivity for MLP and AE (E8).
export CUDA_VISIBLE_DEVICES=""
for s in 0 1 2; do
  python scripts/run_anomaly.py --splits splits/family_seed$s --only P1__ P3__ --detectors lightgbm_energy --contamination 0 --seed $s --out results/revision/lgbm_energy_family_seed$s.csv
  for mode in dedupnone dedupmajority; do
    python scripts/run_anomaly.py --splits splits__$mode/family_seed$s --only P1__ P3__ --detectors ae --contamination 0 --seed $s --out results/revision/ae_${mode}_family_seed$s.csv
    python scripts/run_neural.py --model mlp --splits splits__$mode/family_seed$s --only P1__ P3__ --contamination 0 --epochs 30 --lr 1e-3 --seed $s --out results/revision/mlp2k_${mode}_family_seed$s.csv
  done
  echo "batch1 seed $s done $(date +%H:%M)"
done
