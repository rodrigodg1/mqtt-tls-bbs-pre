#!/bin/bash


for i in {1..4}
do
    echo "Execution $i/100"
    #sleep 5
    python3 publisher.py

done