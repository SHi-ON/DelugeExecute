#!/usr/bin/env python
from sys import argv
from syslog import syslog
syslog('deluge test: the script started running')
for arg in argv[1:]:
    syslog(arg)
