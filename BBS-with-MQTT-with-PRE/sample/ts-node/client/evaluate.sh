#!/bin/bash

killall python3


echo "Removing Last Evaluation ..."

rm -rf ../sub_topic_A/2_subs/sub_A_*
rm -rf ../sub_topic_A/4_subs/sub_A_*
rm -rf ../sub_topic_A/6_subs/sub_A_*
rm -rf ../sub_topic_A/8_subs/sub_A_*
rm -rf ../sub_topic_A/all_delay*

rm -rf ../sub_topic_B/2_subs/sub_B_*
rm -rf ../sub_topic_B/4_subs/sub_B_*
rm -rf ../sub_topic_B/6_subs/sub_B_*
rm -rf ../sub_topic_B/8_subs/sub_B_*
rm -rf ../sub_topic_B/all_delay*

#closes the clients process
killall python3



#header for delay file
echo "Subscribers, Delay (ms)" >> ../sub_topic_A/all_delay_topic_A.csv
echo "Subscribers, Delay (ms)" >> ../sub_topic_B/all_delay_topic_B.csv




#broker process to re-ecnrypt

python3 broker-reencription-subA.py &
python3 broker-reencription-subB.py &


sleep 6



echo "Starting 2 Subs Evaluation ... "
echo -n "2 Subscribers" > n_of_subs.txt
#2 subs per topic
for i in {1..2}
do
    #process client
    python3 sub_re_enc_TOPIC_A.py  &
    python3 sub_re_enc_TOPIC_B.py  &

done

./run_publisher.sh
sleep 5
killall python3

python3 broker-reencription-subA.py &
python3 broker-reencription-subB.py &



echo "Starting 4 Subs Evaluation ... "
echo -n "4 Subscribers" > n_of_subs.txt
#4 subs per topic
for i in {1..4}
do

    python3 sub_re_enc_TOPIC_A.py  &
    python3 sub_re_enc_TOPIC_B.py  &

done

./run_publisher.sh
sleep 5
killall python3

python3 broker-reencription-subA.py &
python3 broker-reencription-subB.py &



echo "Starting 6 Subs Evaluation ... "
echo -n "6 Subscribers" > n_of_subs.txt
#6 subs per topic
for i in {1..6}
do


    python3 sub_re_enc_TOPIC_A.py >> ../sub_topic_A/6_subs/sub_A_$i.csv &
    python3 sub_re_enc_TOPIC_B.py >> ../sub_topic_B/6_subs/sub_B_$i.csv &

done


./run_publisher.sh
sleep 5
killall python3

python3 broker-reencription-subA.py &
python3 broker-reencription-subB.py &




#8 subs per topic
echo "Starting 8 Subs Evaluation ... "
echo -n "8 Subscribers" > n_of_subs.txt
for i in {1..8}
do
  
    python3 sub_re_enc_TOPIC_A.py >> ../sub_topic_A/8_subs/sub_A_$i.csv &
    python3 sub_re_enc_TOPIC_B.py >> ../sub_topic_B/8_subs/sub_B_$i.csv &

done

./run_publisher.sh
sleep 5
killall python3


echo -n "" > n_of_subs.txt
