import paho.mqtt.client as mqtt
import pickle
import pprint
import json
from datetime import datetime



broker = "localhost"
broker_port = 8883


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("temp_with_suburb")
   # client.subscribe("temp_with_gps")

    

# The callback for when a PUBLISH message is received from the server.


#is delegation key send via particular topic between pre and publisher ?
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    received_data = json.loads(msg.payload)
    #print(all_data)
    
    temperature = received_data['Temperature']
    capsule_temp = received_data['Capsule_Temperature']
    suburb = received_data['Suburb']
    capsule_sub_urb = received_data['Capsule_Suburb']
    #proof_temp_suburb = received_data['Proof_Temp_Suburb']
    publisher_time_stamp = received_data['Publisher_Timestamp']
    #server_label = received_data['Server']

    
    end_time =  datetime.now()
    

    publisher_start_time = received_data['Publisher_Timestamp']
    publisher_start_time = publisher_start_time.split(" ")
    publisher_start_time = publisher_start_time[1].split(":")
    publisher_start_time_minute = publisher_start_time[1]
    publisher_start_time_seconds = publisher_start_time[2]


    end_time= str(datetime.now())
    end_time = end_time.split(" ")
    end_time = end_time[1].split(":")
    end_time_minute = end_time[1]
    end_time_seconds = end_time[2]


    delay_minutes = float(end_time_minute) - float(publisher_start_time_minute)
    delay_seconds = float(end_time_seconds) - float(publisher_start_time_seconds)

    #delay = end_time - start_time
    print(publisher_start_time)
    print(publisher_start_time_minute)
    print(publisher_start_time_seconds)


    print(end_time)
    print(end_time_minute)
    print(end_time_seconds)
    

   # pprint.pprint(all_data)

    print("Delay: ", delay_seconds ," seconds")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, broker_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()