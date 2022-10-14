import paho.mqtt.client as mqtt
import ssl
from datetime import datetime
import paho.mqtt.publish as publish
import json
import string
import random
import os
  


TLS_CERT_PATH = "certs/ca/ca.crt"
client_cert = "client/client.crt"
broker_endpoint = "localhost"
port = 8883
key = "client/client.key"



client = mqtt.Client()

#client.on_publish = on_publish
client.tls_set(ca_certs=TLS_CERT_PATH, certfile=client_cert,
                    keyfile=key, cert_reqs=ssl.CERT_REQUIRED,
                    tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)


client.tls_insecure_set(True)


client.connect(broker_endpoint, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()

#def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
 #   return ''.join(random.choice(chars) for _ in range(size))

#id = id_generator()
pid = os.getpid()

f = open("transaction_id.txt", "w")
f.write(str(pid))
f.close()



f = open("transaction_id.txt", "r")
id = f.read()



now = datetime.now()


temperature = '78'
GPS_Lat = '30'
GPS_Long = '123'
Suburb = '2398'


all_data = {
    "id": id,
    "Temperature": temperature,
    "GPS_Lat": GPS_Lat,
    "GPS_Long": GPS_Long,
    "Suburb": Suburb,
    "Publisher_Timestamp":str(now)
}


all_data = json.dumps(all_data)



client.publish("alldata",all_data)

