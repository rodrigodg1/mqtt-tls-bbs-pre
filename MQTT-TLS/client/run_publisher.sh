#!/bin/bash




for i in {1..5}
do
    echo "Execution $i/5"
    sleep 1
    node publisher.js

done