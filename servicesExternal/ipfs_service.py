import ipfsapi
import json

from config import config

# Note to contributers: to work on this you will need to use
# Python's asyncio module most likely

class Ipfs:

    _instance = None

    @staticmethod
    def init(publicIpfs: bool=True):
        Ipfs._instance = Ipfs(publicIpfs)

    @staticmethod
    def getInstance():
        return Ipfs._instance

    def __init__(self, publicIpfs: bool=True):
        self.ipfsConfig = config["ipfs"]["nodeUrlDefault"]["public" if publicIpfs else "private"]
        self.ipfs = ipfsapi.connect(self.ipfsConfig["host"], self.ipfsConfig["port"], self.ipfsConfig["protocol"])

    async def addFile(self, data: str):
        if data == None or data == "":
            raise ValueError("")
        
        data_parsed = json.loads(data)
        result = await self.ipfs.add(json.dumps(data_parsed, separators=(',',':')))

        return result["hash"]

    async def getFile(self, hash: str):
        if hash == None or hash == "":
            raise ValueError("")
        
        try:
            result = await self.ipfs.cat(hash)

            return result
        except ipfsapi.exceptions.Error as err:
            raise err
         

