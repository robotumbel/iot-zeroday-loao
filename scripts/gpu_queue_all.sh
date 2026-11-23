#!/bin/bash
# Full GPU queue for the revision (E9, E14 SecBERT, E11 encoders). Waits until PID $1 (other project's queue) exits.
cd "$(dirname "$0")/.."
bash scripts/gpu_queue_revision.sh "${1:-0}" > logs/gpu_queue_part1.log 2>&1
bash scripts/gpu_queue_e11.sh > logs/gpu_queue_e11.log 2>&1
