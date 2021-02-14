#!/usr/bin/env python
import sys
import os


import syslog as sl
from syslog import syslog
#logging.basicConfig(filename='example.log', level=logging.DEBUG)

sl.openlog(logoption=sl.LOG_DEBUG)
syslog('deluge test: the script started running')

for arg in sys.argv[1:]:
    syslog(arg)

arg_id = sys.argv[1]
arg_name = sys.argv[2]
arg_path = sys.argv[3]

arg_name = arg_name.strip()
arg_path = arg_path.strip()

#os.system('su centos')
#syslog('user id: ' + str(os.getuid()))

# os.system('rsync -arvzh {0}/{1} {user}@{host}:{path}'.format(
#     arg_path, arg_name, user='', host='', path=''))

# syslog('finished uploading to the local machine')

sl.closelog()

