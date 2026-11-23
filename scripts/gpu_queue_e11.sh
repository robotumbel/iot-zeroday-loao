#!/bin/bash
# E11 (GPU part): encoders on the new splits. Starts after GPU queue part 1 has finished.
until grep -q "GPU queue part 1 done" logs/gpu_queue_part1.log 2>/dev/null; do sleep 300; done
until [ -f splits4/family_seed2/index.csv ]; do sleep 60; done
for s in 0 1 2; do
  S="--splits splits4/family_seed$s --only unsw cicids --seed $s"
  python scripts/run_neural.py $S --model tiny-local --scheme sentence --epochs 3 --batch-size 64 --lr 3e-4 --out results/e11/l1_tiny-local_family_seed$s.csv > logs/e11_tiny_seed$s.log 2>&1
  for M in distilbert secbert; do
    python scripts/run_neural.py $S --model $M --scheme sentence --out results/e11/l1_${M}_family_seed$s.csv > logs/e11_${M}_seed$s.log 2>&1
  done
  echo "e11 gpu seed $s done $(date '+%d %H:%M')"
done
echo "E11 GPU done $(date '+%d %H:%M')"
