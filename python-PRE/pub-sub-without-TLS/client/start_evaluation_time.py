
from datetime import datetime


now = datetime.now()

#label  = f"Start Time Evaluation: {now}"

f = open("evaluation/start_time_evaluation.txt", "a")
f.write(str(now))
f.write("\n")
f.close()

