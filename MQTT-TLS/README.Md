## MQTT and TLS

A implementation using mosquitto server and MQTT JS library with TLS connection.


## Instructions

  

### Install mosquitto server:

```console
sudo apt update
sudo apt install -y mosquitto
```

  
  

### Install MQTT JS

  

```console
npm install mqtt --save
```

  
  
  

### Execution

  
  

**Run the broker server:**

```console
cd server/
mosquitto -c server-config.conf
```

  

**Subscriber:**

```console
cd client/
node subscriber.js
```

and **Publisher:**


```console
cd client/
node publisher.js
```