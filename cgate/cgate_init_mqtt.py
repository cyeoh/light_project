#!/usr/bin/python

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import cgate

HOSTNAME='192.168.1.254'
HOSTPORT=20023
PROJNAME='YEOH2'
NETID=254
MQTT_HOSTNAME='192.168.1.254'

# Connect to cgate
cgate_conn = cgate.CGate(HOSTNAME, HOSTPORT, PROJNAME, NETID)
cgate_conn.connect()

for i in range(0, 34):
    lvl = int(cgate_conn.level(i))
    if lvl == 255:
        state = 'on'
    else:
        state = 'off'
    print "Init: %s %s" % (i, state)
    publish.single('lights/%s/state' % i,
                   state, hostname=MQTT_HOSTNAME,
                   protocol=mqtt.MQTTv31, retain=True)
        

