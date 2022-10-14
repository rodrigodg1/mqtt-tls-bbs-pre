#!/bin/bash

killall python3
echo -n "" > n_of_subs.txt



echo "Removing Last Evaluation ..."
sleep 3

rm -rf evaluation/delay*
rm -rf evaluation/start*
rm -rf evaluation/end*




#header for delay file
echo "PID, Clients, Delay (ms)" >> evaluation/delay.csv
echo -n "32 Pubs and Subs " > n_of_subs.txt



echo "Starting 32 Publisher and Subscribers Evaluation ... "


#18 subs process
for i in {1..32}
do
    #process client
    python3 subscriber.py  &
    #./run_publisher.sh &


done

sleep 2



python3 start_evaluation_time.py
for i in {1..32}
do
    #process client
    ./run_publisher.sh &

done




