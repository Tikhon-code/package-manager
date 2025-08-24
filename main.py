#!/bin/python
import requests
import sys

def load(to_file, file):
    print(f"{to_file}{file}")
    URL = requests.get(f"http://192.168.1.100:8000/repository/{to_file}{file}")
    with open(f"files/{file}", 'wb') as f:
        f.write(URL.content)

    

def load_packages(for_file, file):
    with open(f"{for_file}{file}", 'r') as f:
        for line in f:
            load('packages/', line.strip())

    

def main(file):
    try:
        load('info/', f"{file}.info")
        load_packages('files/', f"{file}.info")
    except Exception as e:
        print(e)

if len(sys.argv[1:]) >= 1:
    main(sys.argv[1])