import paho.mqtt.client as mqtt
from umbral import generate_kfrags
from umbral import encrypt, decrypt_original, reencrypt
from umbral import SecretKey, Signer
import paho.mqtt.publish as publish
import json
import pickle

from datetime import datetime


broker = "localhost"
broker_port = 8883


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+ str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("temp_with_suburb")
    client.subscribe("temp_with_gps")


    # The callback for when a PUBLISH message is received from the server.


    # is delegation key send via particular topic between pre and publisher ?
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    received_data = json.loads(msg.payload)
    # print(all_data)

    #print(received_data['Publisher_Timestamp'])


    alices_secret_key = SecretKey.random()
    alices_public_key = alices_secret_key.public_key()

    alices_signing_key = SecretKey.random()
    alices_signer = Signer(alices_signing_key)
    alices_verifying_key = alices_signing_key.public_key()

    # Generate Umbral keys for Bob.
    #sub_a_secret_key = SecretKey.random()
    #sub_a_public_key = sub_a_secret_key.public_key()

    # Generate Umbral keys for Bob.
    sub_b_secret_key = SecretKey.random()
    sub_b_public_key = sub_b_secret_key.public_key()


    # Encrypt data with Alice's public key.

    temperature = '78'
    temperature = temperature.encode()

    GPS_Lat = '30'
    GPS_Lat = GPS_Lat.encode()

    GPS_Long = '123'
    GPS_Long = GPS_Long.encode()

    Suburb = '2398'
    Suburb = Suburb.encode()

    capsule_temp, temp_ciphertext = encrypt(alices_public_key, temperature)
    capsule_gps_lat, gps_lat_ciphertext = encrypt(alices_public_key, GPS_Lat)
    capsule_gps_long, gps_long_ciphertext = encrypt(alices_public_key, GPS_Long)
    capsule_suburb, suburb_ciphertext = encrypt(alices_public_key, Suburb)
    # Decrypt data with Alice's private key.
    #cleartext = decrypt_original(alices_secret_key, capsule, ciphertext)

    



    # create a delegation key for sub B
    kfrags_sub_B = generate_kfrags(delegating_sk=alices_secret_key,
                                receiving_pk=sub_b_public_key,
                                signer=alices_signer,
                                threshold=1,
                                shares=1)





    cfrags_temp = list()          
    for kfrag_sub_B in kfrags_sub_B[:1]:
        cfrag = reencrypt(capsule=capsule_temp, kfrag=kfrag_sub_B)
        cfrags_temp.append(cfrag)    


    cfrags_gps_lat = list()          
    for kfrag_sub_B in kfrags_sub_B[:1]:
        cfrag = reencrypt(capsule=capsule_gps_lat, kfrag=kfrag_sub_B)
        cfrags_gps_lat.append(cfrag)    


    cfrags_gps_long = list()          
    for kfrag_sub_B in kfrags_sub_B[:1]:
            cfrag = reencrypt(capsule=capsule_gps_long, kfrag=kfrag_sub_B)
            cfrags_gps_long.append(cfrag)    


    cfrags_suburb = list()          
    for kfrag_sub_B in kfrags_sub_B[:1]:
            cfrag = reencrypt(capsule=capsule_suburb, kfrag=kfrag_sub_B)
            cfrags_suburb.append(cfrag)   




    all_reencrypted_to_B = {
        "Temperature_ReEnc": str(cfrags_temp),
        "GPS_Lat_ReEnc": str(gps_lat_ciphertext),
        "GPS_Long_ReEnc": str(gps_long_ciphertext),
        "Suburb_ReEnc": str(suburb_ciphertext),
        #"Delegation_key_sub_a": str(kfrags_sub_A),
        #"Delegation_key_sub_b": str(kfrags_sub_B),
        #"Capsule_Temperature": str(capsule_temp),
        #"Capsule_GPS_lat": str(capsule_gps_lat),
       # "Capsule_GPS_long": str(capsule_gps_long),
        #"Capsule_Suburb": str(capsule_suburb),
        "Publisher_Timestamp": received_data['Publisher_Timestamp']
    }

    

    all_reencrypted_to_B = json.dumps(all_reencrypted_to_B)


    publish.single("temp_with_gps_re",all_reencrypted_to_B,hostname=broker, port=broker_port)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, broker_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
