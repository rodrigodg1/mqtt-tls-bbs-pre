
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

# Generate Umbral keys for Bob.
sub_a_secret_key = SecretKey.random()
sub_a_public_key = sub_a_secret_key.public_key()

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


#create a delegation key for sub A
kfrags_sub_A = generate_kfrags(delegating_sk=alices_secret_key,
                         receiving_pk=sub_a_public_key,
                         signer=alices_signer,
                         threshold=1,
                         shares=1)

#create a delegation key for sub B
kfrags_sub_B = generate_kfrags(delegating_sk=alices_secret_key,
                         receiving_pk=sub_b_public_key,
                         signer=alices_signer,
                         threshold=1,
                         shares=1)

now = datetime.now()

all_data = {
    "temperature": str(temp_ciphertext),
    "gps_Lat": str(gps_lat_ciphertext),
    "gps_Long": str(gps_long_ciphertext),
    "suburb": str(suburb_ciphertext),
    "delegation_key_sub_a": str(kfrags_sub_A),
    "delegation_key_sub_b": str(kfrags_sub_B),
    "temp_capsule": str(capsule_temp),
    "gps_lat_capsule": str(capsule_gps_lat),
    "gps_long_capsule": str(capsule_gps_long),
    "capsule_suburb": str(capsule_suburb),
    "publisher_timestamp":str(now)
}
#print(all_data)

all_data_send = json.dumps(all_data)
 


#publish.single("alldata", pickle.dumps(all_data),hostname=broker, port=broker_port)
publish.single("alldata",all_data_send,hostname=broker, port=broker_port)

#publish.single("teste2", "hi",hostname=broker, port=broker_port)