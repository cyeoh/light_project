import os
import signal
import atexit
import re
import threading
import paho.mqtt.client as mqtt

MQTT_HOSTNAME='192.168.1.254'

light_index_info = {
	     0: "chris office",
	     1: "dining ",
	     2: "lounge ",
	     3: "kitchen",
	     4: "island bench",
	     5: "pantry",
	     6: "play room",
	     7: "bathroom",
	     8: "hallway",
	     9: "bed 4",
	     10: "bed 3",
	     11: "bed 2",
	     12: "front door wall lights",
	     13: "garage door wall lights",
	     14: "laundry door",
	     15: "garage",
	     16: "entry dls",
	     17: "kelly office",
	     18: "entry 2 dl",
	     19: "laundry",
	     20: "ensuite exhaust fan",
	     21: "ensuite north dl",
	     22: "ensuite centre dl",
	     24: "ensuite south dl",
	     25: "wir",
	     26: "sinks area dl",
	     27: "toilet exhaust fan",
	     28: "toilet light",
	     29: "bathroom exhaust fan",
	     30: "main bed",
	     31: "alfresco",
	     34: "hallway office"
    }    


from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


dataLock = threading.Lock()
light_data = {}

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/echo/', methods=['GET'])
def echo():
    ret_data = {"value": request.args.get('echoValue')}
    return jsonify(ret_data)

def add_light_row(curr, id):
    color = 'FF0000'
    new_state = 1
    if id in light_data:
        if light_data[id] == 'on':
            color = '00FF00'
            new_state = 0
        line = "<tr><td><a style=\"text-decoration:none;\" href=\"\" onclick=\"toggle_val(%(light_id)s, %(new_state)s); return false;\"><font color=\"000000\"> %(light_name)s</font></a></td><td align=centre><font color=\"%(color)s\">%(state)s</td></tr>" % {
            'color': color, 'light_name': light_index_info[id],
            'state': light_data[id], 'light_id': id, 'new_state': new_state}
        curr += line
    return curr
        


@app.route('/light_data/', methods=['GET'])
def get_light_data():
    output = "<table><tr><th>Light</th><th>Current State</th></tr>"
    
    for id in light_data:
        if id in light_index_info:
            # Note we hide some (power circuits)
            output = add_light_row(output, id)
    output += "</table>"
#    print output
    return output

@app.route('/light_set/', methods=['GET'])
def set_light_data():
    global mqtt_conn
#    print request.args
    id = int(request.args['light'])
    state = int(request.args['lightstate'])
#    print (id, state)
    if state:
        new_state = 'on'
    else:
        new_state = 'off'
#    print (id, new_state)
    mqtt_conn.publish('lights/%(id)s/set_state' % {'id': id}, new_state)

    # Cheat a bit here, assuming that the light state change will succeed and
    # we're not out of date!
    light_data[id] = new_state
    return ("", 204)

# The callback for when the client receives a CONNACK response from the server.
def on_mqtt_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print "Connected to MQTT Server"
    client.subscribe("lights/+/state")

# The callback for when a PUBLISH message is received from the server.
def on_mqtt_message(client, userdata, msg):
    global light_data
    print msg.topic
    m = re.search('lights/(\d+)/state', msg.topic)
    if m:
        id = int(m.group(1))
        light_data[id] = msg.payload
#    print "DEBUG: ", light_data
#    print "DEBUG: ", msg.topic

def interrupt():
    global mqtt_conn
    print "Disconnecting from MQTT"
    mqtt_conn.loop_stop()



if __name__ == '__main__':
# Connect to mqtt
    global mqtt_conn
    global mqtt_thread_var
    mqtt_conn = mqtt.Client(protocol=mqtt.MQTTv31)
    mqtt_conn.on_connect = on_mqtt_connect
    mqtt_conn.on_message = on_mqtt_message
    mqtt_conn.connect(MQTT_HOSTNAME)

    mqtt_conn.loop_start()
    
    atexit.register(interrupt)
    app.run(host='0.0.0.0', port=8080, debug=True)

    mqtt_conn.loop_stop()

