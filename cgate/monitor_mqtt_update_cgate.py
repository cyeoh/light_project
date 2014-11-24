#!/usr/bin/python

import re

import paho.mqtt.client as mqtt
import cgate

HOSTNAME='192.168.1.254'
HOSTPORT=20023
PROJNAME='YEOH2'
NETID=254
MQTT_HOSTNAME='192.168.1.254'

# The callback for when the client receives a CONNACK response from the server.
def on_mqtt_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print "Connected to MQTT Server"
    client.subscribe("lights/+/set_state")

# The callback for when a PUBLISH message is received from the server.
def on_mqtt_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    m = re.search('lights/(\d+)/set_state', msg.topic)
    id = int(m.group(1))
    if msg.payload.lower() == 'on':
        cgate_conn.on(id)
    elif msg.payload.lower() == 'off':
        cgate_conn.off(id)
    else:
        print "Unknown State: ", msg.payload()
    


# Connect to cgate
cgate_conn = cgate.CGate(HOSTNAME, HOSTPORT, PROJNAME, NETID)
cgate_conn.connect()

# Connect to mqtt
mqtt_conn = mqtt.Client(protocol=mqtt.MQTTv31)
mqtt_conn.on_connect = on_mqtt_connect
mqtt_conn.on_message = on_mqtt_message

mqtt_conn.connect(MQTT_HOSTNAME)
mqtt_conn.loop_forever()
