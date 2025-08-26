#!/bin/python
from modules import (
        Timer,
        Unzip,
        Loader,
        System,

        argv,
        argc
    )  

class PackageManager():
    def run(self, action, *args):
        timer = Timer()
        if action == 'install':
            for file in args:
                load = Loader()
                load.load('info/', file, 'info')
                load.load_packages(file, "info")
                unzip = Unzip()
                unzip.unpack()
        timer.end()
        timer.print()


if __name__ == "__main__":
    try:
        if argc > 2:
            packagemanager = PackageManager()
            packagemanager.run(argv[1], *argv[2:])
    except Exception as e:
        print(f"Program breaked, error: {e}")
        System.exit(1)
