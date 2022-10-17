#!/bin/bash

killall -9 python3
echo -n "" > n_of_subs.txt



echo "Removing Last Evaluation ..."
sleep 3

rm -rf evaluation/delay*
rm -rf evaluation/start*
rm -rf evaluation/end*



#python3 broker-reencription-subA.py &
python3 broker-reencription-subB.py &


echo "Starting 4 Publisher and Subscribers Evaluation ... "

#header for delay file

echo "PID, Clients, Delay (ms)" >> evaluation/delay.csv
echo -n "16 Pubs and Subs " > n_of_subs.txt
sleep 4

for i in {1..16}
do
    #process client
    #python3 sub_re_enc_TOPIC_A.py  &
    python3 sub_re_enc_TOPIC_B.py  &

done

sleep 2




#for TPS calculation
python3 start_evaluation_time.py
for i in {1..16}
do
    #process client
    ./run_publisher.sh &

done




