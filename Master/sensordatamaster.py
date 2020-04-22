# import paho.mqtt.client as mqtt
from thingspeak import * as ts

class JSONParser(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)

class Packet(object):
    def __init__(self, payload):
        packet_data = JSONParser(payload)
        self.name = packet_data.name
        self.ID = packet_data.id
        self.Value = packet_data.value

class Room(object):
    def __init__(self, room_data):
        data = JSONParser(room_data)
        self.name = data.name
        self.LDR = data.ldr_id
        self.DHT = data.dht_id
        self.darkIntensityValue = data.darkIntensityValue
        self.lightIntensityValue = data.ligtIntensityValue


slaapkamer = Room()

client = Thin



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