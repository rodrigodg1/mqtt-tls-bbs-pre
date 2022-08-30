import paho.mqtt.client as mqtt
import ssl


TLS_CERT_PATH = "certs/ca/ca.crt"
client_cert = "client/client.crt"
broker_endpoint = "localhost"
port = 1333
key = "client/client.key"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("temp_with_suburb")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect

#client.on_publish = on_publish
client.tls_set(ca_certs=TLS_CERT_PATH, certfile=client_cert,
                    keyfile=key, cert_reqs=ssl.CERT_REQUIRED,
                    tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)


client.tls_insecure_set(False)



client.on_message = on_message

client.connect("localhost", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()