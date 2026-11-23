#!/bin/bash
# Revision batch 2 (CPU): E1 temporal control, E2 two-stage, E13 robust windows, E7 unfiltered P3, E10 chronological P1.
export CUDA_VISIBLE_DEVICES=""
for s in 0 1 2; do
  for e in temporal twostage robust popen chrono; do
    python scripts/run_revision_rf.py --exp $e --splits splits/family_seed$s --seed $s --out results/revision/${e}_family_seed$s.csv
  done
  echo "batch2 seed $s done $(date +%H:%M)"
done
