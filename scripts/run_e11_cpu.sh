#!/bin/bash
# E11 (CPU part): four-dataset splits and every CPU detector on the new splits (those that involve
# NF-UNSW-NB15-v3 or NF-CICIDS2018-v3). Splits that involve only ToN/BoT are identical to the paper's.
export CUDA_VISIBLE_DEVICES=""
until [ -f data/processed/nf_cicids2018_v3__cap20000__seed2.stats.json ]; do sleep 60; done
sleep 30
for s in 0 1 2; do
  python -m loao.cli splits --processed "data/processed/nf_*__cap20000__seed$s.parquet" --protocols P1 P3 --level family --seed $s --out splits4
done
for s in 0 1 2; do
  S="--splits splits4/family_seed$s --only unsw cicids --seed $s"
  python scripts/run_baseline_rf.py $S --norm none --contamination 0 0.05 --n-estimators 100 --out results/e11/rf_msp_full_family_seed$s.csv > /dev/null 2>&1
  python scripts/run_baseline_rf.py $S --norm none --contamination 0 0.05 --n-estimators 100 --max-train-per-unit 2000 --calib far warmup --out results/e11/rf_msp_cap2000_family_seed$s.csv > /dev/null 2>&1
  python scripts/run_neural.py $S --model mlp --epochs 30 --lr 1e-3 --max-train-per-unit 2000 --out results/e11/mlp_cap2000_family_seed$s.csv > logs/e11_mlp2k_seed$s.log 2>&1
  python scripts/run_neural.py $S --model mlp --epochs 30 --lr 1e-3 --max-train-per-unit 0 --out results/e11/mlp_full_family_seed$s.csv > logs/e11_mlpfull_seed$s.log 2>&1
  python scripts/run_anomaly.py $S --out results/e11/anomaly_family_seed$s.csv > logs/e11_anomaly_seed$s.log 2>&1
  python scripts/run_baselines_extra.py $S --out results/e11/extra_baselines_family_seed$s.csv > logs/e11_extra_seed$s.log 2>&1
  echo "e11 cpu seed $s done $(date '+%d %H:%M')"
done
