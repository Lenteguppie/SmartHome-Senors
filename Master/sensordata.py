# import paho.mqtt.client as mqtt
from thingspeak import *
import json

import urllib3
import time


READ_API_KEY='YOUR READ API KEY'
CHANNEL_ID= 'YOUR CHANNEL ID'

class Packet(object):
    def __init__(self, payload):
        print (payload)
        self.created_at = payload["created_at"]
        self.entry_id = payload["entry_id"]
        self.name = payload["field1"]
        self.id = payload["field2"]
        self.value = payload["field3"]
    
    def print(self):
        print("Packet --> \"Name: {0}, ID: {1}, Value: {2}\"".format(self.name, self.id, self.value))

class Room(object):
    def __init__(self, room_data):
        self.name = room_data['name']
        self.LDR = room_data['ldr_id']
        self.darkIntensityValue = room_data['darkIntensityValue']
        self.lightIntensityValue = room_data['ligtIntensityValue']
    
    def print(self):
        print("Room --> \"name: {0}, LDR_ID: {1}, Dark: {2}, Light: {3}\"".format(self.name, self.LDR, self.darkIntensityValue, self.lightIntensityValue))
    
def get_room_data():
    with open('room.json') as json_file:
        room_data = json.load(json_file)
        print('Name: ' + room_data['name'])
        print('LDR_ID: ' + room_data['ldr_id'])
        print('darkIntensityValue: ' + str(room_data['darkIntensityValue']))
        print('ligtIntensityValue: ' + str(room_data['ligtIntensityValue']))
        print('')
        return room_data

def get_last_packet():

    http = urllib3.PoolManager()
    url = "http://api.thingspeak.com/channels/{}/feeds/last.json?api_key={}".format(CHANNEL_ID,READ_API_KEY)
    r = http.request('GET', url)
    data = None
    data_len = 0

    data = json.loads(r.data.decode('utf-8'))
    data_len = len(data)

    return Packet(data)

slaapkamer = Room(get_room_data())
slaapkamer.print()

while True:
    new_packet = get_last_packet()
    print(new_packet.id)
    if (new_packet != None ):
        if (new_packet.id == slaapkamer.LDR):
            print("slaapkamer LDR :D")

    time.sleep(5)


'''
The functions for sending and/ or receiving the data with MQTT

'''

# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))

#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     client.subscribe("LightIntensity/#")

# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     # print(msg.topic+" "+str(msg.payload))
#     parse_message(msg)


# client = mqtt.Client(client_id="HASSIO_LightIntensity_Manager")
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect("localhost", 1883, 60)

# # Blocking call that processes network traffic, dispatches callbacks and
# # handles reconnecting.
# # Other loop*() functions are available that give a threaded interface and a
# # manual interface.
# client.loop_forever()