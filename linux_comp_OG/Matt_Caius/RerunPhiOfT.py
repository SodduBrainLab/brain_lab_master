import time
import sys
from subprocess import Popen


currentTime = time.time()
RunTime = currentTime

print(currentTime)
print(RunTime)

filename = r"/home/brainlab/PycharmProjects/brain_lab/Matt_Caius"
print(filename)

while True:
    if RunTime <= currentTime:
        print("Restarting PhiofT")
        p = Popen("python " + filename,shell = True)
        RunTime += 2*60*60