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

const mqtt = require("mqtt");
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
  key: KEY,
  cert: CERT,
  rejectUnauthorized: false,
  // The CA list will be used to determine if server is authorized
  ca: TRUSTED_CA_LIST,
  protocol: "mqtts",
};

import {
  generateBls12381G2KeyPair,
  blsSign,
  blsVerify,
  blsCreateProof,
  blsVerifyProof,
} from "@mattrglobal/bbs-signatures";
import { exit } from "process";

const main = async () => {
  try {


    const client = mqtt.connect(options);

    const keyPair = await generateBls12381G2KeyPair();


    //document sent by publisher and will be received by server
    let jsonInputDocument = require("../inputDocument.json");

    const temperature = jsonInputDocument.Data.Temperature;
    const suburb = jsonInputDocument.Data.Suburb;
    const latitude = jsonInputDocument.Data.GPS_Lat;
    const longitude = jsonInputDocument.Data.GPS_Long;

    //Set of messages we wish to sign
    const messages = [
      Uint8Array.from(Buffer.from(temperature.toString(), "utf8")),
      Uint8Array.from(Buffer.from(suburb.toString(), "utf8")),
      Uint8Array.from(Buffer.from(latitude.toString(), "utf8")),
      Uint8Array.from(Buffer.from(longitude.toString(), "utf8")),
    ];

    //publisher time
    var startTime_publisher = new Date().toISOString();

    //publisher creates the signature. The signature and the inputDocument will be send to the server.
    const signature = await blsSign({
      keyPair,
      messages: messages,
    });


    var data_signature = {
      Temperature: temperature,
      Suburb: suburb,
      Latitude: latitude,
      Longitude: longitude,
      //Signature: signature,
      Timestamp: startTime_publisher,
      Server: false
    };
    var data_signature_string = JSON.stringify(data_signature);


    //publish the data
    client.publish("signature_data", data_signature_string);


  } catch (error) {
    console.error(error);
  }

  setTimeout(function () {
    exit();
  }, 1000);
};

main();
