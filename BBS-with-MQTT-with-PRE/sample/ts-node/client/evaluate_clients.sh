#!/bin/bash

killall -9 python3
killall node
echo -n "" > n_of_subs.txt



echo "Removing Last Evaluation ..."
sleep 3

rm -rf evaluation/delay*
rm -rf evaluation/start*
rm -rf evaluation/end*



#python3 broker-reencription-subA.py &
python3 broker-reencription-subB.py &


echo "Starting 8 Publisher and Subscribers Evaluation ... "

#header for delay file

echo "PID, Clients, Delay (ms)" >> evaluation/delay.csv
echo -n "4 Pubs and Subs " > n_of_subs.txt
sleep 4

for i in {1..4}
do
    #process client
    #python3 sub_re_enc_TOPIC_A.py  &
    python3 sub_re_enc_TOPIC_B.py  &

done

sleep 2


./run_server-and-verifier.sh

sleep 2



python3 start_evaluation_time.py
for i in {1..4}
do
    #process client
    ./run_publisher.sh &

done




