#!/usr/bin/python

import cgate

import time

conn = cgate.CGate('192.168.1.254', 20023, 'YEOH2', 254)

conn.connect()

while True:
    print "light on"
    conn.on(0)
    print conn.level(0)
    time.sleep(2)
    print "light off"
    conn.off(0)
    print conn.level(0)
    time.sleep(2)
