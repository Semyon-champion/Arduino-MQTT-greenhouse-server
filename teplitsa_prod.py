#!/usr/bin/python2.7
import paho.mqtt.client as mqtt
import  psycopg2
import json
import time

#dictionary
#{"type":"sr","id":"1","ms":"at","value":"NULL"} = 1
#{"type":"sr","id":"1","ms":"ah","value":"NULL"} = 2
#{"type":"sr","id":"2","ms":"at","value":"NULL"} = 3
#{"type":"sr","id":"2","ms":"ah","value":"NULL"} = 4
#{"type":"sr","id":"3","ms":"at","value":"NULL"} = 5
#{"type":"sr","id":"3","ms":"ah","value":"NULL"} = 6
#{"type":"sr","id":"4","ms":"at","value":"NULL"} = 7
#{"type":"sr","id":"4","ms":"ah","value":"NULL"} = 8
#{"type":"sr","id":"5","ms":"at","value":"NULL"} = 9
#{"type":"sr","id":"5","ms":"ah","value":"NULL"} = 10
#{"type":"sr","id":"6","ms":"sh","value":"NULL"} = 11
#{"type":"sr","id":"7","ms":"sh","value":"NULL"} = 12
#{"type":"rl","id":"1","ms":"ht","value":"NULL"} = 13
#{"type":"rl","id":"2","ms":"sw","value":"NULL"} = 14


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#    client.subscribe("$SYS/#")
#    client.subscribe("esp/test")
#    client.subscribe("test", 2)
#    client.subscribe("REQUESTS", 2)
    client.subscribe("REQUESTS", 2)
    client.subscribe("test", 2)
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print("on topic:"+msg.topic+"  received message:"+str(msg.payload))
    sensdata=json.loads(msg.payload.decode('utf-8'))
    if sensdata['info'][0]['type']=='sr' and sensdata['info'][0]['id']=='1':
        info['1']=sensdata['info'][0]['value']
        info['2']=sensdata['info'][1]['value']
    elif sensdata['info'][0]['type']=='sr' and sensdata['info'][0]['id']=='2':
        info['3']=sensdata['info'][0]['value']
        info['4']=sensdata['info'][1]['value']
    elif sensdata['info'][0]['type']=='sr' and sensdata['info'][0]['id']=='3':
        info['5']=sensdata['info'][0]['value']
        info['6']=sensdata['info'][1]['value']
    elif sensdata['info'][0]['type']=='sr' and sensdata['info'][0]['id']=='4':
        info['7']=sensdata['info'][0]['value']
        info['8']=sensdata['info'][1]['value']
    elif sensdata['info'][0]['type']=='sr' and sensdata['info'][0]['id']=='5':
        info['9']=sensdata['info'][0]['value']
        info['10']=sensdata['info'][1]['value']
    elif sensdata['info'][1]['type']=='sr' and sensdata['info'][1]['id']=='7':
        info['11']=sensdata['info'][1]['value']

    curtime = time.time()
    if (curtime>userdata.printtime+1200):
#       print "vot ono:", time.strftime('%x %X')
#       print info
       userdata.printtime=time.time()
       cursor.execute("insert into sensors (internal_temp1, internal_temp2, internal_temp3, internal_temp4, external_temp1, internal_hum1,internal_hum2,internal_hum3,internal_hum4,external_hum1, seq_hum1, datetime) values ("+info['1']+","+info['3']+","+info['5']+","+info['7']+","+info['9']+","+info['2']+","+info['4']+","+info['6']+","+info['8']+","+info['10']+","+info['11']+",'"+time.strftime('%d.%m.%Y %H:%M:%S')+"' )")
       DBconn.commit()

class USERDATA:
  def __init__(self, printtime):
     self.printtime=printtime

ud=USERDATA(time.time())

info={"1":"NULL","2":"NULL","3":"NULL","4":"NULL","5":"NULL","6":"NULL","7":"NULL","8":"NULL","9":"NULL","10":"NULL","11":"NULL","12":"NULL","13":"NULL","14":"NULL"}

client = mqtt.Client(userdata=ud)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set('ivswvecv', password='Epnb9MlZFfvU')
client.connect("m20.cloudmqtt.com", 15516, 15)

DBconn = psycopg2.connect(host='localhost', user='postgres', password='postgres', dbname='sequoia')
cursor = DBconn.cursor()
#lient.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


