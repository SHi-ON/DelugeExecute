#!/bin/sh

if [ `pgrep -f sentry.py` ];
then
    echo "### Sentry is already running!!"
    exit 1
else
    nohup nice bash -c "/home/ubuntu/miniconda3/envs/Ni9er/bin/python sentry.py" &
    exit 0
fi
