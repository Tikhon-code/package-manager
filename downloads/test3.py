from modules.globals import to_unzip
import threading
import asyncio
import aiohttp
import aiofiles

class Loader():
    def load(self, *args):
        asyncio.run(self.load_file(*args))

    def load_packages(self, *args):
        asyncio.run(self.load_packages_from_file(*args))

    async def load_file(self, for_file, file, typefile=None, url=f"https://raw.githubusercontent.com/Tikhon-code/package-manager-repo/refs/heads/main/"):
        if typefile != None:
            file = f"{file}.{typefile}"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}{for_file}{file}") as response:
                if response.status == 200:
                    print(f"{file}: OK")
                else:
                    print(f"{file}: ERROR {response.status}")
                    return 1
            
                if file.endswith('.zip'):
                    self.__body = await response.read()
                    async with aiofiles.open(f"downloads/{file}", 'wb') as f:
                        await f.write(self.__body)
                        return to_unzip.append(f"downloads/{file}")
                else:
                    self.__body = await response.text()  
                    async with aiofiles.open(f"downloads/{file}", 'w') as f:
                        await f.write(self.__body)  
                    

    async def load_packages_from_file(self, file, type, *args):
        threads = []
        async with aiofiles.open(f"downloads/{file}.{type}") as f:
            async for line in f:
                line = line.strip()
                thread = threading.Thread(target=self.load, args=('packages/', line))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
