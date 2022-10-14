#!/bin/bash


#python3 start_evaluation_time.py


for i in {1..100}
do
    echo "Execution $i/100"
    
    python3 publisher.py 
    sleep 1

done


#python3 end_evaluation_time.py

