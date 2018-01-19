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
    def get_instance():
        return Ipfs._instance

    def __init__(self, publicIpfs: bool=True):
        self.ipfsConfig = config["ipfs"]["nodeUrlDefault"]["public" if publicIpfs else "private"]
        self.ipfs = ipfsapi.connect(self.ipfsConfig["host"], self.ipfsConfig["port"], self.ipfsConfig["protocol"])

    async def add_file(self, data: str):
        if data is None or data == "":
            raise ValueError("Data is None or invalid.")
        
        data_parsed = json.loads(data)
        result = await self.ipfs.add(json.dumps(data_parsed, separators=(',',':')))

        return result["hash"]

    async def get_file(self, hash: str):
        if hash is None or hash == "":
            raise ValueError("Hash is None or invalid.")
        
        try:
            result = await self.ipfs.cat(hash)

            return result
        except ipfsapi.exceptions.ConnectionError as err:
            print("IPFS connection error: ", err)
        except ipfsapi.exceptions.ProtocolError as err:
            print("Bad connection protocol: ", err)
        except ipfsapi.exceptions.ErrorResponse as err:
            print("Error retrieving file: ", err)
        except ipfsapi.exceptions.StatusError as err:
            print("Status error: ", err)
        except ipfsapi.exceptions.TimeoutError as err:
            print("Connection timeout error: ", err)
        except ipfsapi.exceptions.Error as err:
            print("Error retrieving file: ", err)
        finally:
            return None