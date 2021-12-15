#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh # Or path to where your conda is
conda activate base
cd /home/d2esr/python/pyvpgn-monitor
python srvcheck.py >> srvcheck.log
python pending_check.py >> srvcheck.log
