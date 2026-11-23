#!/bin/bash
# GPU queue for the first-round revision. Waits until the other project's GPU queue (PID given as $1) exits.
WAIT_PID=${1:-0}
if [ "$WAIT_PID" != "0" ]; then
  while powershell -Command "Get-Process -Id $WAIT_PID -ErrorAction SilentlyContinue" > /dev/null 2>&1 && \
        powershell -Command "if (Get-Process -Id $WAIT_PID -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"; do
    sleep 300
  done
fi
echo "GPU queue start $(date '+%d %H:%M')"
# E9: training length, seed 0, P1, DistilBERT and SecBERT (6 epochs, per-epoch evaluation)
for m in distilbert secbert; do
  python scripts/run_epochs.py --splits splits/family_seed0 --only P1__ --model $m --epochs 6 --seed 0 --out results/revision/epochs_${m}_family_seed0.csv
  echo "E9 $m seed0 done $(date '+%d %H:%M')"
done
# E14: SecBERT with an explicit 'missing' token, splits that contain NF-BoT-IoT-v3
for s in 0 1 2; do
  python scripts/run_neural.py --splits splits/family_seed$s --only P1__nf_bot P3__ --model secbert --scheme sentence --nan-token --contamination 0 --seed $s --out results/revision/l1_secbert-nan_family_seed$s.csv
  echo "E14 seed$s done $(date '+%d %H:%M')"
done
echo "GPU queue part 1 done $(date '+%d %H:%M')"
