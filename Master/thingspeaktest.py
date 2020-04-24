import urllib3
import json
import time

'''
Test to get data from Thingspeak
'''


READ_API_KEY='YOUR READ API KEY'
CHANNEL_ID= 'YOUR CHANNEL ID'

http = urllib3.PoolManager()
url = "http://api.thingspeak.com/channels/{}/feeds/last.json?api_key={}".format(CHANNEL_ID,READ_API_KEY)
r = http.request('GET', url)

data = json.loads(r.data.decode('utf-8'))
print("Data --> {}".format(data))
data_len = len(data)
print(r.status)

print(data_len)