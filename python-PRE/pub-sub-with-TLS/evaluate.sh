#!/bin/bash

killall python3


echo "Removing Last Evaluation ..."

rm -rf evaluation/delay*
rm -rf evaluation/total*

#closes the clients process
killall python3



#header for delay file
echo "Subscribers, Delay (ms)" >> evaluation/delay.csv




echo "Starting 8 Subs Evaluation ... "
sleep 3

echo -n "8 Subscribers" > n_of_subs.txt
#2 subs process
for i in {1..8}
do
    #process client
    python3 subscriber.py  &
    #python3 sub_re_enc_TOPIC_B.py  &

done

./run_publisher.sh
sleep 5
killall python3



echo "Starting 32 Subs Evaluation ... "
sleep 3

echo -n "32 Subscribers" > n_of_subs.txt
#4 subs per topic
for i in {1..32}
do

    python3 subscriber.py  &
   # python3 sub_re_enc_TOPIC_B.py  &

done

./run_publisher.sh
sleep 5
killall python3


echo "Starting 128 Subs Evaluation ... "

sleep 3
echo -n "128 Subscribers" > n_of_subs.txt
#6 subs per topic
for i in {1..128}
do

    python3 subscriber.py  &
    #python3 sub_re_enc_TOPIC_A.py >> ../sub_topic_A/6_subs/sub_A_$i.csv &
    #python3 sub_re_enc_TOPIC_B.py >> ../sub_topic_B/6_subs/sub_B_$i.csv &

done


./run_publisher.sh
sleep 5
killall python3




#8 subs per topic
echo "Starting 8 Subs Evaluation ... "
echo -n "8 Subscribers" > n_of_subs.txt
for i in {1..8}
do
    python3 subscriber.py  &
    #python3 sub_re_enc_TOPIC_A.py >> ../sub_topic_A/8_subs/sub_A_$i.csv &
    #python3 sub_re_enc_TOPIC_B.py >> ../sub_topic_B/8_subs/sub_B_$i.csv &

done

./run_publisher.sh
sleep 5
killall python3


echo -n "" > n_of_subs.txt
