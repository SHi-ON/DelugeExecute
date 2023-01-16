#!/bin/sh

if [ "$(pgrep -f sentry.py)" ]; then
  if [ "$1" = "-r" ]; then
    echo "####### restarting Sentry..."

    echo "# kill Sentry"
    kill -9 `pgrep -laf sentry.py | awk '{print $1}'`
    rm nohup.out

    sleep 2

    echo "# run Sentry"
    nohup nice bash -c "~/miniconda3/envs/WebDev9/bin/python sentry.py" &
    echo ""
    exit 0
  else
    echo "##### Sentry is already running!!"
    exit 1
  fi
else
  echo "### run Sentry"
  nohup nice bash -c "~/miniconda3/envs/WebDev9/bin/python sentry.py" &
  echo ""
  exit 0
fi
