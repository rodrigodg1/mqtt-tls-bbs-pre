#!/bin/bash

cd ..

yarn server-bbs &
yarn sub-a-verifier &
yarn sub-b-verifier &

cd client/

for i in {1..50}
do
    echo "Execution $i/50"
    sleep 5
    python3 publisher.py

done