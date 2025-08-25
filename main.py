#!/bin/python

import concurrent.futures
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


async def load(for_file, file):
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
                    

async def load_packages(file):
    files = []
    with open(f'downloads/{file}', 'r') as f:
        for line in f:
            files.append(line.strip())

    tasks = [load('packages/', file) for file in files if file.strip() != '']
    await asyncio.gather(*tasks)


async def unzip_zip():
    for zip in to_unzip:
        print(f"Unpacking: {zip}")
        with zipfile.ZipFile(zip, 'r') as zipf:
            zipf.extractall(f'downloads/')


def main(file, *args):
    start() 
    if asyncio.run(load('info/', f"{file}.info")) != 1:
        asyncio.run(load_packages(f"{file}.info"))
        if to_unzip != []:
            asyncio.run(unzip_zip())
    print(end())


if len(sys.argv) > 1:
    main(sys.argv[1])
