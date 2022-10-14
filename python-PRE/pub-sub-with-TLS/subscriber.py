import paho.mqtt.client as mqtt
import ssl
from datetime import datetime
import paho.mqtt.publish as publish
import json





TLS_CERT_PATH = "certs/ca/ca.crt"
client_cert = "client/client.crt"
broker_endpoint = "localhost"
port = 8883
key = "client/client.key"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("alldata")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    received_data = json.loads(msg.payload)
    print(received_data)



    end_time =  datetime.now()
    
    publisher_id_transaction = received_data['id']

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
    #print(publisher_start_time)
    #print(publisher_start_time_minute)
    #print(publisher_start_time_seconds)


    #print(end_time)
    #print(end_time_minute)
   # print(end_time_seconds)
    

   # pprint.pprint(all_data)

    #print("Delay: ", delay_seconds*1000 ," ms")

    delay_ms = delay_seconds*1000
    delay_ms = "%.2f" %delay_ms

    #print(delay_ms)


    f = open("n_of_subs.txt", "r")
    #print(f.read())
    n_of_subs = f.read()


    n_of_subs_delay_ms = f"{publisher_id_transaction},{n_of_subs},{delay_ms}"
    n_of_subs_delay_ms = str(n_of_subs_delay_ms)

    #print(n_of_subs_delay_ms)

    f = open("evaluation/delay.csv", "a")
    f.write(str(n_of_subs_delay_ms))
    f.write("\n")
    f.close()




    f = open("evaluation/end_evaluation_time.txt", "a")
    f.write(str(datetime.now()))
    f.write("\n")
    f.close()







client = mqtt.Client()
client.on_connect = on_connect

#client.on_publish = on_publish
client.tls_set(ca_certs=TLS_CERT_PATH, certfile=client_cert,
                    keyfile=key, cert_reqs=ssl.CERT_REQUIRED,
                    tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)


client.tls_insecure_set(True)


client.on_message = on_message

client.connect("localhost", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()