file = open("evaluation/delay.csv", "r")
line_count = 0
for line in file:
    if line != "\n":
        line_count += 1
file.close()


#without header
total_transactions = line_count
#print(line_count-1)


f = open("evaluation/start_time_evaluation.txt", "r")
start_time = f.read()


f = open("evaluation/end_evaluation_time.txt", "r")
end_time = f.readlines()[-1]




publisher_start_time = start_time.split(" ")
publisher_start_time = publisher_start_time[1].split(":")
publisher_start_time_minute = publisher_start_time[1]
publisher_start_time_seconds = publisher_start_time[2]



end_time = end_time.split(" ")
end_time = end_time[1].split(":")
end_time_minute = end_time[1]
end_time_seconds = end_time[2]


delay_minutes = float(end_time_minute) - float(publisher_start_time_minute)
delay_seconds = float(end_time_seconds) - float(publisher_start_time_seconds)



delay_ms = delay_seconds*1000
delay_ms = "%.2f" %delay_ms


total_delay_in_s = (delay_minutes*60) + delay_seconds


print("Total Transactions: ",total_transactions)
print("Total Time (s): ",total_delay_in_s)
print("TPS:", total_transactions/total_delay_in_s)
