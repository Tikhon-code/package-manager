from modules.globals import to_unzip
import threading
import zipfile
import datetime
import sys
import os


class Timer():
    def __init__(self):
        self.start()

    def start(self):
        
        self.now = datetime.datetime.now()

    def end(self):
        self.end = datetime.datetime.now()
        self.result = self.end - self.now
        return self.result

    def print(self, variable='result'):
        exec(f'print(self.{variable})')

class Unzip:
    def unzip_zip(self, archive, *args):
        print(f"Unpacking: {archive}")
        with zipfile.ZipFile(archive, 'r') as zipf:
            for zip in zipf.namelist():
                print("extracting", zip)
                zipf.extract(zip)

    def unpack(self):
        self.threads = []
        for zip in to_unzip:
            self.thread = threading.Thread(target=self.unzip_zip, args=(zip,))
            self.thread.start()
            self.threads.append(self.thread)

        for thread in self.threads:
            thread.join()

class System():
    def exit(code=0):
        sys.exit(code)
    
    def remove(path):
        os.remove(path)