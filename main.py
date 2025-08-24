#!/bin/python
import requests
import zipfile
import sys
import os


def load(to_file, file):
    print(f"Downloading: {file}")
    URL = requests.get(f"https://raw.githubusercontent.com/Tikhon-code/package-manager/refs/heads/main/repository/{to_file}{file}", stream=True)
    if URL.status_code == 200:
        with open(f"files/{file}", 'wb') as f:
            f.write(URL.content)

    else:
        print(f"File: {file} not found in {to_file}")
        return 1

    

def load_packages(for_file, file):
    with open(f"{for_file}{file}", 'r') as f:
        for line in f:
            load('packages/', line.strip())
            if line.strip().endswith('zip'):
                with zipfile.ZipFile(f"{for_file}{line}".strip(), 'r') as zip:
                    zip.extractall(for_file)
                os.remove(f"{for_file}{line}".strip())

    
def main(file):
    if load('info/', f"{file}.info") != 1:
        load_packages('files/', f"{file}.info")
        os.remove(f'files/{file}.info')

if len(sys.argv[1:]) >= 1:
    main(sys.argv[1])
