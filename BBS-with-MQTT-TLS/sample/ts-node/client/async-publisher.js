"use strict";

//const mqtt = require('mqtt')
const MQTT = require("async-mqtt");
const fs = require("fs");
const path = require("path");
const { exit } = require("process");
const KEY = fs.readFileSync(path.join(__dirname, "/client.key"));
const CERT = fs.readFileSync(path.join(__dirname, "/client.crt"));
const TRUSTED_CA_LIST = fs.readFileSync(path.join(__dirname, "/ca.crt"));

const PORT = 8883;
const HOST = "localhost";

const options = {
  port: PORT,
  host: HOST,
  key: KEY,
  cert: CERT,
  rejectUnauthorized: false,
  // The CA list will be used to determine if server is authorized
  ca: TRUSTED_CA_LIST,
  protocol: "mqtts",
};

run();

async function run() {
  const client = await MQTT.connectAsync(options);

  console.log("Starting");

  var t0 = new Date().toISOString();
  const temp_with_suburb_object = {
    Temperature: "82",
    Suburb: "2398",
    Timestamp: t0,
  };
  var temp_with_suburb = JSON.stringify(temp_with_suburb_object);

  try {
    await client.publish("temp_with_suburb", temp_with_suburb);
    // This line doesn't run until the server responds to the publish
    await client.end();
    // This line doesn't run until the client has disconnected without error
    console.log("Done");
  } catch (e) {
    // Do something about it!
    console.log(e.stack);
    process.exit();
  }
}
