import paho.mqtt.client as mqtt
import pickle
import pprint
import json

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
    all_data = json.loads(msg.payload)
    #print(all_data)
    
    temperature = all_data['Temperature']
    capsule_temp = all_data['Capsule_Temperature']
    suburb = all_data['Suburb']
    capsule_sub_urb = all_data['Capsule_Suburb']
    proof_temp_suburb = all_data['Proof_Temp_Suburb']
    publisher_time_stamp = all_data['Publisher_Timestamp']
    server_label = all_data['Server']

    print(server_label)
    

    #pprint.pprint(all_data)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, broker_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()