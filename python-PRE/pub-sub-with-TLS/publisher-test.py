import paho.mqtt.client as mqtt
import ssl

import paho.mqtt.publish as publish


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


client.tls_insecure_set(False)

client.connect(broker_endpoint, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()

client.publish("teste","aeee")