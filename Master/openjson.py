import json

with open('room.json') as json_file:
    data = json.load(json_file)
    print('Name: ' + data['name'])
    print('LDR_ID: ' + data['ldr_id'])
    print('DHT_ID: ' + data['dht_id'])
    print('darkIntensityValue: ' + str(data['darkIntensityValue']))
    print('ligtIntensityValue: ' + str(data['ligtIntensityValue']))
    print('')