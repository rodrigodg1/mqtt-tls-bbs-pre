
from umbral import generate_kfrags
from umbral import encrypt, decrypt_original
from umbral import SecretKey, Signer
import paho.mqtt.publish as publish
import json
import pickle
from datetime import datetime




broker = "localhost"
broker_port = 8883


# In this implementation, we are assuming thar publisher know subs through public keys.


alices_secret_key = SecretKey.random()
alices_public_key = alices_secret_key.public_key()

alices_signing_key = SecretKey.random()
alices_signer = Signer(alices_signing_key)
alices_verifying_key = alices_signing_key.public_key()

# Generate Umbral keys for User A.
sub_a_secret_key = SecretKey.random()
sub_a_public_key = sub_a_secret_key.public_key()

# Generate Umbral keys for User B.
sub_b_secret_key = SecretKey.random()
sub_b_public_key = sub_b_secret_key.public_key()



temperature = '78'
temperature = temperature.encode()

GPS_Lat = '30'
GPS_Lat = GPS_Lat.encode()

GPS_Long = '123'
GPS_Long = GPS_Long.encode()

Suburb = '2398'
Suburb = Suburb.encode()


#encrypt the items
capsule_temp, temp_ciphertext = encrypt(alices_public_key, temperature)
capsule_gps_lat, gps_lat_ciphertext = encrypt(alices_public_key, GPS_Lat)
capsule_gps_long, gps_long_ciphertext = encrypt(alices_public_key, GPS_Long)
capsule_suburb, suburb_ciphertext = encrypt(alices_public_key, Suburb)
# Decrypt data with Alice's private key.
#cleartext = decrypt_original(alices_secret_key, capsule, ciphertext)


#create a delegation key for sub A
#kfrags_sub_A = generate_kfrags(delegating_sk=alices_secret_key,
#                         receiving_pk=sub_a_public_key,
 #                        signer=alices_signer,
#                         threshold=1,
 #                        shares=1)

#create a delegation key for sub B
kfrags_sub_B = generate_kfrags(delegating_sk=alices_secret_key,
                         receiving_pk=sub_b_public_key,
                         signer=alices_signer,
                         threshold=1,
                         shares=1)

now = datetime.now()


'''
temp_suburb_data = {

    "Temperature": str(temp_ciphertext),
    "Suburb": str(suburb_ciphertext),
    "Capsule_Temperature": str(capsule_temp),
    "Capsule_Suburb": str(capsule_suburb),
    "Publisher_Timestamp":str(now)

}

'''

all_data = {
    "Temperature": str(temp_ciphertext),
    "GPS_Lat": str(gps_lat_ciphertext),
    "GPS_Long": str(gps_long_ciphertext),
    "Suburb": str(suburb_ciphertext),
    #"Delegation_key_sub_a": str(kfrags_sub_A),
    "Delegation_key_sub_b": str(kfrags_sub_B),
    "Capsule_Temperature": str(capsule_temp),
    "Capsule_GPS_lat": str(capsule_gps_lat),
    "Capsule_GPS_long": str(capsule_gps_long),
    "Capsule_Suburb": str(capsule_suburb),
    "Publisher_Timestamp":str(now)
}
#print(all_data)

#temp_suburb_data = json.dumps(temp_suburb_data)
#temp_with_gps_data = json.dumps(temp_with_gps_data)
all_data = json.dumps(all_data)


#publish.single("alldata", pickle.dumps(all_data),hostname=broker, port=broker_port)
#publish.single("temp_with_suburb",temp_suburb_data,hostname=broker, port=broker_port)

publish.single("alldata",all_data,hostname=broker, port=broker_port)

#publish.single("temp_with_gps",temp_with_gps_data,hostname=broker, port=broker_port)
#publish.single("teste2", "hi",hostname=broker, port=broker_port)