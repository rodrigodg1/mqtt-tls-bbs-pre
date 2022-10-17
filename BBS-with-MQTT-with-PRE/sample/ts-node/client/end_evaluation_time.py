
from datetime import datetime



now = datetime.now()

label  = f"End Time Evaluation: {now}"

f = open("evaluation/total_time_evaluation.txt", "a")
f.write(str(label))
f.write("\n")
f.close()

