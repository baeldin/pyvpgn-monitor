#!/bin/bash
set -x
source ~/miniconda3/etc/profile.d/conda.sh # Or path to where your conda is
conda activate base
cd /home/d2esr/python/pyvpgn-monitor
if [ $# -eq 1 ]; then
  python restart.py -N $1
else
  python restart.py
fi
