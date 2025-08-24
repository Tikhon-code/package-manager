#!/bin/python
import subprocess
import datetime
import requests
import zipfile
import asyncio
import sys
import os


def start(startind=0):
    global now
    now = datetime.datetime.now()


def end():
    end = datetime.datetime.now()
    return end - now


def show_packages(for_file, file):
    print("To install:")
    with open(f"{for_file}{file}", 'r') as f:
        for line in f:
            line = line.strip()
            print(line)

def load(to_file, file, sub=False):
    global process
    if sub == False:
        os.system(f'lua request.lua {to_file} {file}')
    else:
        process = subprocess.Popen(['lua', 'request.lua', to_file, file])
    


async def load_packages(for_file, file):
    show_packages(for_file, file)
    with open(f"{for_file}{file}", 'r') as f:
        for line in f:
            line = line.strip()
            load('packages/', file=line, sub=True)
            if line.endswith('zip'):
                process.wait()
                print(f"extracting: {line}")
                
                with zipfile.ZipFile(f"{for_file}{line}", 'r') as zip:
                    zip.extractall(for_file)
                

                print(f"deleting source zip file: {line}")
                os.remove(f"{for_file}{line}")


def main(file):
    start()
    load('info/', f"{file}.info", False)
    asyncio.run(load_packages('files/', f"{file}.info"))
    os.remove(f'files/{file}.info')
    print(f"Downloading complete, finish time: {end()}")

if len(sys.argv[1:]) >= 1:
    main(sys.argv[1])
