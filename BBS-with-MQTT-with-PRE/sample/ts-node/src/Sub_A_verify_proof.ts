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
    client.subscribe("temp_with_suburb");



    client.on("message", async function (topic, message) {
      console.log("\nReceived Data:")

      //console.log(message.toString())
      
      const received_data_from_publisher = JSON.parse(message.toString());

      console.log(received_data_from_publisher)

      
      const temperature = received_data_from_publisher["Temperature"];
      const suburb = received_data_from_publisher["Suburb"];
      const timestamp_from_publisher = received_data_from_publisher["Publisher_Timestamp"]




      //console.log("Temperature: ", temperature)
      //console.log("Suburb: ", suburb)
      //console.log("Signature: ", signature)
      console.log("Publisher Timestamp: ", timestamp_from_publisher)



      const messages = [
        Uint8Array.from(Buffer.from(temperature.toString(), "utf8")),
        Uint8Array.from(Buffer.from(suburb.toString(), "utf8")),
      ];


      const signature = await blsSign({
        keyPair,
        messages: messages,
      });
  

      
    //Verify the signature
    /*
    const isVerified = await blsVerify({
      publicKey: keyPair.publicKey,
      messages: messages,
      signature,
    });
    */

  

    //create a proof for first version

    const proof_temp_suburb = await blsCreateProof({
      signature,
      publicKey: keyPair.publicKey,
      messages,
      nonce: Uint8Array.from(Buffer.from("nonce", "utf8")),
      revealed: [0, 1], //temperature and suburb position and capsules
    });
   

    const isProofVerified = await blsVerifyProof({
      proof:proof_temp_suburb,
      publicKey: keyPair.publicKey,
      messages: messages.slice(0, 2),
      nonce: Uint8Array.from(Buffer.from("nonce", "utf8")),
    });
    console.log("Proof Temp_Suburb: ", isProofVerified )

    

    //create a object with version 2 to send to the subscribers
    var temp_suburb = {
      Temperature: temperature,
      Suburb: suburb,
      Proof_Temp_Suburb: proof_temp_suburb,
      Publisher_Timestamp: timestamp_from_publisher,
      Server:true
    };
    var temp_with_suburb_string = JSON.stringify(temp_suburb);


    


    client.publish("temp_with_suburb_verified", temp_with_suburb_string);



    console.log("Published !");


    });




  } catch (error) {
    console.error(error);
  }




};


main()
