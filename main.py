#!/bin/python

from multiprocessing import Process
import datetime
import asyncio
import aiohttp
import aiofiles
import zipfile
import sys
import os


to_unzip = []


def start():
    global now
    now = datetime.datetime.now()


def end():
    end = datetime.datetime.now()
    return end - now


async def load(for_file, file, type=None):
    if type != None:
        file = f"{file}.{type}"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://raw.githubusercontent.com/Tikhon-code/package-manager/refs/heads/main/repository/{for_file}{file}") as response:
            if response.status == 200:
                print(f"{file}: OK")
            else:
                print(f"{file}: ERROR {response.status}")
                return 1
            
            if file.endswith('.zip'):
                body = await response.read()
            else:
                body = await response.text()
            if file.endswith('.zip'):
                async with aiofiles.open(f"downloads/{file}", 'wb') as f:
                    await f.write(body)
                    return to_unzip.append(f"downloads/{file}")
                    
            else:
                async with aiofiles.open(f"downloads/{file}", 'w') as f:
                    await f.write(body)
                    

async def load_packages(file, type, *args):
    file2 = f"{file}.{type}"
    files = []
    with open(f'downloads/{file2}', 'r') as f:
        for line in f:
            files.append(line.strip())

    tasks = [load('packages/', file) for file in files if file.strip() != '']
    await asyncio.gather(*tasks)


def unzip_zip():
    for zip in to_unzip:
        print(f"Unpacking: {zip}")
        with zipfile.ZipFile(zip, 'r') as zipf:
            zipf.extractall('downloads/')


def main(action, *args):
    start() 
    if action == 'install':
        for file in args:
            if asyncio.run(load('info/', file, 'info')) != 1:
                asyncio.run(load_packages(file, "info"))
                if to_unzip != []:
                    processes = []
                    p = Process(target=unzip_zip)
                    processes.append(p)
                    p.start()
                    p.join()
                    
    print(end())


try:
    if len(sys.argv) > 2:
        main(sys.argv[1], *sys.argv[2:])
except Exception as e:
    print(f"Program breaked, time: {end()}, error: {e}")