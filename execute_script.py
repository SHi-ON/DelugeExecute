from sys import argv
from syslog import syslog

syslog('SHi-ON deluge execute test: the script started running...')

for arg in argv:
	syslog(arg)