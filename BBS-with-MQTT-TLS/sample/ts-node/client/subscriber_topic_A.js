"use strict";

const mqtt = require("mqtt");
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

const client = mqtt.connect(options);

client.subscribe("temp_with_suburb");

client.on("message", function (topic, message) {
  //console.log("\nReceived Data:")

  console.log(message.toString())

  const temp_with_suburb_object = JSON.parse(message);

  const temperature = temp_with_suburb_object["Temperature"];
  const suburb = temp_with_suburb_object["Suburb"];
  const server_label = temp_with_suburb_object["Server"];
  const t0 = temp_with_suburb_object["Timestamp"].toString();

  // 2022-07-10T18:30:08.671Z

  const started_time = t0.split(":");
  const started_minute = t0[1];
  const started_time_seconds_and_ms = started_time[2].slice(0, 6);


  console.log("\nServer Label: ", server_label)
  console.log("Timestamp received: " + t0)
  const current_time = new Date().toISOString();
  console.log("Current Time:       " + current_time)
  const end_time = current_time.split(":");
  const end_minute = end_time[1];
  const end_time_seconds_and_ms = end_time[2].slice(0, 6);

  var delay = (end_time_seconds_and_ms - started_time_seconds_and_ms) * 1000;
  console.log("Delay in ms: ", delay.toFixed(2))

  fs.readFile("n_of_subs.txt", "utf8", function (err, data) {
    if (err) {
      return console.log(err);
    }
    var n_subs = data;
    //console.log(data + ", " + delay.toFixed(2));
  });
});
