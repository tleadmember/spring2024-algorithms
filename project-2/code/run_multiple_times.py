import subprocess
import sys

numTimes = 8
# only give the sys 2 input the first time
subprocess.run(["python", "improve_output.py", sys.argv[1], sys.argv[2]]) 
for i in range(1, 8):
    subprocess.run(["python", "improve_output.py", sys.argv[1], "0"]) 