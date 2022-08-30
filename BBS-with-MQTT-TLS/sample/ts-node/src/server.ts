/*
 * Copyright 2020 - MATTR Limited
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *     http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

"use strict";

import { readFileSync } from "fs";
const execSync = require("child_process").execSync;

const MQTT = require("mqtt");
const fs = require("fs");
const path = require("path");
const KEY = fs.readFileSync(path.join(__dirname, "/client.key"));
const CERT = fs.readFileSync(path.join(__dirname, "/client.crt"));
const TRUSTED_CA_LIST = fs.readFileSync(path.join(__dirname, "/ca.crt"));

const PORT = 8883;
const HOST = "localhost";

const options = {
  port: PORT,
  host: HOST,
  //key: KEY,
  //cert: CERT,
  rejectUnauthorized: false,
  // The CA list will be used to determine if server is authorized
  //ca: TRUSTED_CA_LIST,
  //protocol: "mqtts",
  protocol: "mqtt"
};

import {
  generateBls12381G2KeyPair,
  blsSign,
  blsVerify,
  blsCreateProof,
  blsVerifyProof,
} from "@mattrglobal/bbs-signatures";
import { exit } from "process";
import { Console } from "console";



const main = async () => {
  try {
    //Generate a new key pair

    const client = MQTT.connect(options);

    const keyPair = await generateBls12381G2KeyPair();


    //console.log("Server Connected")



    //topic between publisher and server
    client.subscribe("alldata");



    client.on("message", async function (topic, message) {
      console.log("\nReceived Data:")

      console.log(message.toString())
      
      const received_data_from_publisher = JSON.parse(message);

      const temperature = received_data_from_publisher["temperature"];
      const suburb = received_data_from_publisher["suburb"];
      const latitude = received_data_from_publisher["gps_Lat"];
      const longitude = received_data_from_publisher["gps_Long"];
      const capsule_temp = received_data_from_publisher["temp_capsule"];
      const capsule_gps_lat = received_data_from_publisher["gps_lat_capsule"];
      const capsule_gps_long = received_data_from_publisher["gps_long_capsule"];
      const capsule_suburb = received_data_from_publisher["capsule_suburb"]
      //const signature = received_data["Signature"];
      const timestamp_from_publisher = received_data_from_publisher["publisher_timestamp"]


      console.log("Temperature: ", temperature)
      console.log("Suburb: ", suburb)
      console.log("Latitude: ", latitude)
      console.log("Longitude: ", longitude)
      console.log("CAP. Temp: ", capsule_temp)
      console.log("CAP. GPS LAT: ", capsule_gps_lat)
      console.log("CAP. GPS LONG: ", capsule_gps_long)
      console.log("CAP. Suburb: ", capsule_suburb)
      //console.log("Signature: ", signature)
      console.log("Publisher Timestamp: ", timestamp_from_publisher)



      const messages = [
        Uint8Array.from(Buffer.from(temperature.toString(), "utf8")),
        Uint8Array.from(Buffer.from(capsule_temp.toString(), "utf8")),
        Uint8Array.from(Buffer.from(suburb.toString(), "utf8")),
        Uint8Array.from(Buffer.from(capsule_suburb.toString(), "utf8")),
        Uint8Array.from(Buffer.from(latitude.toString(), "utf8")),
        Uint8Array.from(Buffer.from(capsule_gps_lat.toString(), "utf8")),
        Uint8Array.from(Buffer.from(longitude.toString(), "utf8")),
        Uint8Array.from(Buffer.from(capsule_gps_long.toString(), "utf8")),
      ];


      const signature = await blsSign({
        keyPair,
        messages: messages,
      });
  

      
    //Verify the signature
    const isVerified = await blsVerify({
      publicKey: keyPair.publicKey,
      messages: messages,
      signature,
    });

  

    //create a proof for first version
    const proof_temp_suburb = await blsCreateProof({
      signature,
      publicKey: keyPair.publicKey,
      messages,
      nonce: Uint8Array.from(Buffer.from("nonce", "utf8")),
      revealed: [0, 1,2,3], //temperature and suburb position and capsules
    });



    //create a object with version 2 to send to the subscribers
    var temp_suburb = {
      Temperature: temperature,
      Capsule_Temperature: capsule_temp,
      Suburb: suburb,
      Capsule_Suburb: capsule_suburb,
      Proof_Temp_Suburb: proof_temp_suburb,
      Publisher_Timestamp: timestamp_from_publisher,
      Server:true
    };
    var temp_with_suburb_string = JSON.stringify(temp_suburb);


    client.publish("temp_with_suburb", temp_with_suburb_string);




    //Derive a proof for second version
    const proof_all_items = await blsCreateProof({
      signature,
      publicKey: keyPair.publicKey,
      messages,
      nonce: Uint8Array.from(Buffer.from("nonce", "utf8")),
      revealed: [0, 1, 2,3,4,5,6,7], //all items and capsules
    });


    //create a object with version 2 to send to the subscribers
    var temp_with_gps = {
      Temperature: temperature,
      Capsule_Temperature: capsule_temp,

      Lat_GPS: latitude,
      Capsule_gps_lat: capsule_gps_lat,

      Long_GPS: longitude,
      Capsule_gps_long: capsule_gps_long,

      Suburb: suburb,
      Capsule_Suburb: capsule_suburb,
      
      Proof_All_Items: proof_all_items,
      Publisher_Timestamp: timestamp_from_publisher,
      Server:true
    };
    var temp_with_gps_json = JSON.stringify(temp_with_gps);




    client.publish("temp_with_gps", temp_with_gps_json);


    console.log("Published !");



    });




  } catch (error) {
    console.error(error);
  }




};


main()
