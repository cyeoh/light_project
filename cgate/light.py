#!/usr/bin/python

HOSTNAME='192.168.1.254'
HOSTPORT=20023
PROJNAME='YEOH2'
NETID=254

import cgate
import sys


id = sys.argv[1]
cmd = sys.argv[2]

conn = cgate.CGate(HOSTNAME, HOSTPORT, PROJNAME, NETID)

conn.connect()

if cmd.lower() == 'on':
    conn.on(id)
elif cmd.lower() == 'off':
    conn.off(id)
elif cmd.lower() == 'get':
    level = conn.level(id)
    print level
else:
    print "unrecognized command cmd: ", cmd
