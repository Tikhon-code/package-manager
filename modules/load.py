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

    async def load_file(self, for_file, file, typefile=None, url=f"https://raw.githubusercontent.com/Tikhon-code/package-manager/refs/heads/main/repository/"):
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
        
        self.file2 = f"{file}.{type}"
        self.files = []
        self.repeat_file = ''
        with open(f'downloads/{self.file2}', 'r') as f:
            for line in f:
                if self.repeat_file == line.strip():
                    continue
                self.repeat_file = line.strip()
                
                self.files.append(line.strip())

        self.tasks = [self.load_file('packages/', file) for file in self.files if file.strip() != '']
        await asyncio.gather(*self.tasks)