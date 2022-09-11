#!/bin/sh

if [ $(pgrep -f sentry.py) ]; then
  echo "### Sentry is already running!!"
  exit 1
else
  nohup nice bash -c "~/miniconda3/envs/WebDev9/bin/python sentry.py" &
  exit 0
fi
