#!/bin/bash



cd ..

yarn server &

for i in {1..5}
do
    echo "Execution $i/5"
    sleep 2
    yarn publisher

done