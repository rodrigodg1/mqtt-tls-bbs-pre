#!/bin/bash



cd ..

yarn server-bbs &
yarn sub-a-verifier &
yarn sub-b-verifier &

for i in {1..100}
do
    echo "Execution $i/100"
    sleep 2
    yarn publisher


done