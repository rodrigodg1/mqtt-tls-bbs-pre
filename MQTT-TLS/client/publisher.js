'use strict'

const mqtt = require('mqtt')
const fs = require('fs')
const path = require('path')
const { exit } = require('process')
const KEY = fs.readFileSync(path.join(__dirname, '/client.key'))
const CERT = fs.readFileSync(path.join(__dirname, '/client.crt'))
const TRUSTED_CA_LIST = fs.readFileSync(path.join(__dirname, '/ca.crt'))

const PORT = 8883
const HOST = 'localhost'

const options = {
  port: PORT,
  host: HOST,
  key: KEY,
  cert: CERT,
  rejectUnauthorized: false,
  // The CA list will be used to determine if server is authorized
  ca: TRUSTED_CA_LIST,
  protocol: 'mqtts'
}

const client = mqtt.connect(options)

//const t0 = performance.now();







function publish_temp_with_suburb(params) {
  

  var t0 = new Date().toISOString()
  const temp_with_suburb_object = { "Temperature": "82", "Suburb": "2398", "Timestamp": t0 }
  var temp_with_suburb = JSON.stringify(temp_with_suburb_object);

  client.publish('temp_with_suburb', temp_with_suburb)


}
function publish_temp_with_gps(params) {
  
  var t0 = new Date().toISOString()
  const temp_with_GPS_object = {"Temperature":"82","GPS-Lat":"30","GPS-Long":"123", "Timestamp": t0 }
  var temp_with_GPS = JSON.stringify(temp_with_GPS_object);


  client.publish('temp_with_gps', temp_with_GPS)



}



publish_temp_with_suburb()
publish_temp_with_gps()





var delayInMilliseconds = 1000; //1 second
setTimeout(function () {
  client.end()
}, delayInMilliseconds);










//client.end()










