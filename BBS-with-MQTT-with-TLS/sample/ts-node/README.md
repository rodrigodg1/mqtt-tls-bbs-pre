# BBS-MQTT-TLS

The publisher sends a document (inputDocument) to the server with the following items to the "signature_data" topic:

- "Temperature",
- "GPS_Lat"
- "GPS_Long"
- "Suburb"

The server received the data and creates a two diferent versions in topics:

- Topic 1: temp_with_suburb
- Topic 2: temp_with_gps

Subscriber A receives the Topic 1 with temperature and Suburb information.

Subscriber B receives the Topic 2 with all informations (i.e., temperature, GPS_Lat, GPS_Long, and Suburb)


## Instructions

Install MQTT:

```
npm install mqtt --save
```

Install mosquitto:

```
sudo apt-get install mosquitto
```

In the mosquitto server:

```
cd server/
```

run the config. file `server-config.conf`:



```
mosquitto -c server-config.conf
```

to run the clients/subscribers:

```
cd client/
```

and

```
node subscriber_topic_A.js
```

in other terminal:

```
node subscriber_topic_B.js
```

To generate the derived proofs run the publisher and server code:

```
yarn install --frozen-lockfile
yarn publisher
```



In other terminal

```
yarn server
```

for automated evaluation, run:

```
cd client/
chmod +x evaluate.sh
./evaluate.sh
```