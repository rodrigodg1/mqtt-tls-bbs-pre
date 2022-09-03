import paho.mqtt.client as mqtt
import pickle
import pprint
import json
from datetime import datetime
from umbral import generate_kfrags
from umbral import encrypt, decrypt_original, reencrypt
from umbral import SecretKey, Signer
from umbral import decrypt_reencrypted



broker = "localhost"
broker_port = 8883


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("temp_with_suburb")
    client.subscribe("temp_with_suburb_re")

    

# The callback for when a PUBLISH message is received from the server.


#is delegation key send via particular topic between pre and publisher ?
def on_message(client, userdata, msg):

    alices_secret_key = SecretKey.random()
    alices_public_key = alices_secret_key.public_key()

    alices_signing_key = SecretKey.random()
    alices_signer = Signer(alices_signing_key)
    alices_verifying_key = alices_signing_key.public_key()

    # Generate Umbral keys for Sub B.
    sub_a_secret_key = SecretKey.random()
    sub_a_public_key = sub_a_secret_key.public_key()


    # Encrypt data with Alice's public key.

    temperature = '78'
    temperature = temperature.encode()

    Suburb = '2398'
    Suburb = Suburb.encode()

    capsule_temp, temp_ciphertext = encrypt(alices_public_key, temperature)
    capsule_suburb, suburb_ciphertext = encrypt(alices_public_key, Suburb)
    # Decrypt data with Alice's private key.
    #cleartext = decrypt_original(alices_secret_key, capsule, ciphertext)

    
    capsule_temp, temp_ciphertext = encrypt(alices_public_key, temperature)
    capsule_suburb, suburb_ciphertext = encrypt(alices_public_key, Suburb)
    # Decrypt data with Alice's private key.
    #cleartext = decrypt_original(alices_secret_key, capsule, ciphertext)

    

    # create a delegation key for sub A
    kfrags_sub_A = generate_kfrags(delegating_sk=alices_secret_key,
                                receiving_pk=sub_a_public_key,
                                signer=alices_signer,
                                threshold=1,
                                shares=1)


    cfrags_temp = list()          
    for kfrag_sub_A in kfrags_sub_A[:1]:
        cfrag = reencrypt(capsule=capsule_temp, kfrag=kfrag_sub_A)
        cfrags_temp.append(cfrag)    


    cfrags_suburb = list()          
    for kfrag_sub_A in kfrags_sub_A[:1]:
            cfrag = reencrypt(capsule=capsule_suburb, kfrag=kfrag_sub_A)
            cfrags_suburb.append(cfrag)   





    temp_cleartext = decrypt_reencrypted(receiving_sk=sub_a_secret_key,
                                        delegating_pk=alices_public_key,
                                        capsule=capsule_temp,
                                        verified_cfrags=cfrags_temp,
                                        ciphertext=temp_ciphertext)

    suburb_cleartext = decrypt_reencrypted(receiving_sk=sub_a_secret_key,
                                        delegating_pk=alices_public_key,
                                        capsule=capsule_suburb,
                                        verified_cfrags=cfrags_suburb,
                                        ciphertext=suburb_ciphertext)




    #print(temp_cleartext)         
    #print(suburb_cleartext)                              


    #print(msg.topic+" "+str(msg.payload))
    received_data = json.loads(msg.payload)
    #print(all_data)


    temperature = received_data['Temperature_ReEnc']
    #capsule_temp = received_data['Capsule_Temperature']
    #capsule_gps_long = received_data['Capsule_GPS_long']
    suburb = received_data['Suburb_ReEnc']
    #capsule_sub_urb = received_data['Capsule_Suburb']
    #proof_all_items = all_data['Proof_All_Items']
    publisher_time_stamp = received_data['Publisher_Timestamp']
    
    #server_label = all_data['Server']

    #pprint.pprint(received_data)

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


    n_of_subs_delay_ms = f"{n_of_subs},{delay_ms}"
    n_of_subs_delay_ms = str(n_of_subs_delay_ms)

    print(n_of_subs_delay_ms)

    f = open("../sub_topic_A/all_delay_topic_A.csv", "a")
    f.write(str(n_of_subs_delay_ms))
    f.write("\n")
    f.close()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, broker_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()