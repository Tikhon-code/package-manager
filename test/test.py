import sys
import os
import subprocess
def arg_parse():
    global loops, to_install
    count = 0
    loops = []
    to_install = []
    for i in sys.argv[1:]:
        count += 1
        if i == "--loops":
            loops.append(sys.argv[count + 1])

        if i == "-i":
            to_install.append(sys.argv[count + 1])

arg_parse()
os.chdir("..")
count = 0
processes = []
while True:
    count += 1
    
    process = subprocess.Popen(["python", "main.py", "install", *to_install])
    print(f"process: {count} started")
    processes.append(process)

    if count == int(loops[0]): break

count = 0
for process in processes:
    count += 1
    process.wait()
    print(f"process: {count} ended")