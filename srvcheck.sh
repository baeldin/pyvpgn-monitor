#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh # Or path to where your conda is
conda activate base
# echo wtf is going on?
echo /home/$(whoami)/miniconda3/bin/python srvcheck.py
cd /home/$(whoami)/python/pyvpgn-monitor
/home/$(whoami)/miniconda3/bin/python srvcheck.py >> srvcheck.log
python pending_check.py >> srvcheck.log
