########################################################################
# App to make sure the lights go on and off if the light intinisty is at a certain value
########################################################################
import json
import hassapi as hass
import urllib3
import time
import datetime

#Thingspeak variabelen
READ_API_KEY='CV5MX1SHMCOD7IKS'
CHANNEL_ID= '1042789'

class Packet(hass.Hass):
    '''
    Als er een pakket ontvangen wordt kan die hier overzichtelijk ingezet worden. 
    Nu kan die ook makkelijk opgeslagen worden voor als je die later wil gebruiken!
    '''
    def __init__(self, payload):
        print (payload)
        self.created_at = payload["created_at"]
        self.entry_id = payload["entry_id"]
        self.name = payload["field1"]
        self.sensor_id = payload["field2"]
        self.value = float(payload["field3"])
    
    def print(self):
        print("Packet --> \"Name: {0}, ID: {1}, Value: {2}\"".format(self.name, self.sensor_id, self.value))

class Room(hass.Hass):
    '''
    class om de variabelen voor de app op te slaan voor een specifieke kamer
    '''
    def __init__(self, name, ldr_id, toggle):
        self.name = name
        self.lamp = "light.lamp_sascha"
        self.LDR = ldr_id
        self.toggleValue = toggle
    
    def print(self):
        print("Room --> \"name: {0}, LDR_ID: {1}, Toggle Value: {2}\"".format(self.name, self.LDR, self.toggleValue))

class SensorData(hass.Hass):
    def initialize(self):
        '''
        Initialisatie voor als appdeamon de app start.
        '''  
        self.old_packet = None
        self.debug = self.args["debug"]
        time = datetime.time(0, 0, 0)
        self.run_minutely(self.pakketdienst, time)
        if (self.debug == 1):
            self.log("SensorData Initiated!")  

        self.slaapkamer = Room(self.args["name"], self.args["ldr_id"], self.args["toggle"])
        self.slaapkamer.print()

    def pakketdienst(self, kwargs):
        '''
        Deze functie verwerkt de paketten zodat met de data het licht aan en uit gezet kan worden
        '''
        new_packet = self.get_last_packet()
            
        if (new_packet != None):
            if (self.args["debug"] == 1):
                self.log("sensor_id: {0}".format(new_packet.sensor_id))
            if (self.args["debug"] == 1):
                self.log("new entry_id: {0}".format(new_packet.entry_id))
            if (self.old_packet != None): 
                if (self.args["debug"] == 1):
                    self.log("old entry id {0} ".format(self.old_packet.entry_id))
            
            if(self.old_packet == None):
                self.old_packet = new_packet
                if (new_packet.sensor_id == self.slaapkamer.LDR):
                    if (self.debug == 1):
                        self.log("LDR matched!")
                    if(int(new_packet.value) >= self.slaapkamer.toggleValue):
                        self.turn_on(self.slaapkamer.lamp)
                    elif (float(new_packet.value) < float(self.slaapkamer.toggleValue)):
                        self.turn_off(self.slaapkamer.lamp)

            if (new_packet.entry_id != self.old_packet.entry_id):
                self.old_packet = new_packet
                if (new_packet.sensor_id == self.slaapkamer.LDR):
                    if (self.debug == 1):
                        self.log("LDR matched!")
                    if(int(new_packet.value) >= self.slaapkamer.toggleValue):
                        self.turn_on(self.slaapkamer.lamp)
                    elif (int(new_packet.value) <= self.slaapkamer.toggleValue):
                        self.turn_off(self.slaapkamer.lamp)
                    
                
            else:
                if (self.args["debug"] == 1):
                    self.log("No new packet found on thingsspeak")
                pass
            
        else:
            if (self.debug == 1):
                self.log("Error while try request to Thingspeak")

    def get_last_packet(self):
        #verkrijg het laatste pakketje van Thingspeak
        http = urllib3.PoolManager()
        url = "http://api.thingspeak.com/channels/{}/feeds/last.json?api_key={}".format(CHANNEL_ID,READ_API_KEY)
        r = http.request('GET', url)
        data = None
        data_len = 0
        if (self.args["debug"] == 1):
            self.log("Status: {}".format(r.status))

        if (r.status == 200): #Check if the request is completed
            data = json.loads(r.data.decode('utf-8'))
            data_len = len(data)
        
            return Packet(data)
        else:
            return None