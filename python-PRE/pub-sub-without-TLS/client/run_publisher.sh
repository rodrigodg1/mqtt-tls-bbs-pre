#!/bin/bash




for i in {1..100}
do
    echo "Execution $i/100"
    sleep 1
    python3 publisher.py

done