#!/bin/sh
# Render on teapot (2x RTX 4090) instead of the laptop, then pull the results into out/.
# usage: ./teapot.sh --shot surf --light golden --samples 40 --scale 50 --frames 432 --out out/surf_golden.png
# Runs under nohup on teapot, so a dropped connection doesn't kill it; rerun the same command to resume.
set -e
cd "$(dirname "$0")"
scp -q scene.py teapot:ocean/
ssh teapot "cd ~/ocean && mkdir -p out && for g in 0 1; do
  CUDA_VISIBLE_DEVICES=\$g nohup ./blender-5.3.0-linux-x64/blender -b -P scene.py -- $* --start \$g --step 2 > render\$g.log 2>&1 &
done; wait; tail -n 3 render0.log render1.log | grep -iE 'error|traceback' || true"
rsync -a teapot:ocean/out/ out/
