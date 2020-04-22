# import paho.mqtt.client as mqtt
from thingspeak import *
import json

# class Packet(object):
#     def __init__(self, payload):
#         packet_data = JSONParser(payload)
#         self.name = packet_data.name
#         self.ID = packet_data.id
#         self.Value = packet_data.value

class Room(object):
    def __init__(self, room_data):
        self.name = room_data['name']
        self.LDR = room_data['ldr_id']
        self.DHT = room_data['dht_id']
        self.darkIntensityValue = room_data['darkIntensityValue']
        self.lightIntensityValue = room_data['ligtIntensityValue']
    
    def print(self):
        print("name: {0}, LDR_ID: {1}, DHT_ID: {2}, Dark: {3}, Light: {4}".format(self.name, self.LDR, self.DHT, self.darkIntensityValue, self.lightIntensityValue))


def get_room_data():
    with open('room.json') as json_file:
        room_data = json.load(json_file)
        print('Name: ' + room_data['name'])
        print('LDR_ID: ' + room_data['ldr_id'])
        print('DHT_ID: ' + room_data['dht_id'])
        print('darkIntensityValue: ' + str(room_data['darkIntensityValue']))
        print('ligtIntensityValue: ' + str(room_data['ligtIntensityValue']))
        print('')
        return room_data


slaapkamer = Room(get_room_data())
slaapkamer.print()



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