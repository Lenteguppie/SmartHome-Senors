########################################################################
# App to make sure the lights go on and off if the light intinisty is at a certain value
########################################################################
import json
import hassapi as hass
import urllib3
import time
import datetime


READ_API_KEY='CV5MX1SHMCOD7IKS'
CHANNEL_ID= '1042789'

class Packet(hass.Hass):
    def __init__(self, payload):
        print (payload)
        self.created_at = payload["created_at"]
        self.entry_id = payload["entry_id"]
        self.name = payload["field1"]
        self.id = payload["field2"]
        self.value = payload["field3"]
    
    def print(self):
        print("Packet --> \"Name: {0}, ID: {1}, Value: {2}\"".format(self.name, self.id, self.value))

class Room(hass.Hass):
    def __init__(self, name, ldr_id, dark, light):
        self.name = name
        self.lamp = "light.lamp_sascha"
        self.LDR = ldr_id
        self.darkIntensityValue = dark
        self.lightIntensityValue = light
    
    def print(self):
        print("Room --> \"name: {0}, LDR_ID: {1}, Dark: {2}, Light: {3}\"".format(self.name, self.LDR, self.darkIntensityValue, self.lightIntensityValue))

class SensorData(hass.Hass):
    def initialize(self):   
        self.debug = self.args["debug"]
        time = datetime.time(0, 0, 0)
        self.run_minutely(self.pakketdienst, time)
        if (self.debug == 1):
            self.log("SensorData Initiated!")  

        self.slaapkamer = Room(self.args["name"], self.args["ldr_id"], self.args["darkIntensityValue"], self.args["ligtIntensityValue"])
        self.slaapkamer.print()

    def pakketdienst(self, kwargs):
        new_packet = self.get_last_packet()
            
        if (new_packet != None):
            print(new_packet.id)
            if (new_packet.id == self.slaapkamer.LDR):
                if (self.debug == 1):
                    self.log("LDR matched!")
                if(int(new_packet.value) >= self.slaapkamer.darkIntensityValue):
                    self.turn_on(self.slaapkamer.lamp)
                elif (int(new_packet.value) <= self.slaapkamer.lightIntensityValue):
                    self.turn_off(self.slaapkamer.lamp)
        else:
            if (self.debug == 1):
                self.log("Error while try request to ThingSpeak")

    def get_last_packet(self):

        http = urllib3.PoolManager()
        url = "http://api.thingspeak.com/channels/{}/feeds/last.json?api_key={}".format(CHANNEL_ID,READ_API_KEY)
        r = http.request('GET', url)
        data = None
        data_len = 0

        print ("Status: {}".format(r.status))

        if (r.status == 200): #Check if the request is completed
            data = json.loads(r.data.decode('utf-8'))
            data_len = len(data)
        
            return Packet(data)
        else:
            return None