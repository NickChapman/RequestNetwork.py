import json

import ipfsapi
from ipfsapi.exceptions import (ConnectionError, Error, ErrorResponse,
                                ProtocolError, StatusError, TimeoutError)

from config import config

# Note to contributers: to work on this you will need to use
# Python's asyncio module most likely


class Ipfs:

    _instance = None

    @staticmethod
    def init(publicIpfs: bool = True):
        Ipfs._instance = Ipfs(publicIpfs)

    @staticmethod
    def get_instance():
        return Ipfs._instance

    def __init__(self, publicIpfs: bool = True):
        self.ipfsConfig = (
            config["ipfs"]["nodeUrlDefault"]
            ["public" if publicIpfs else "private"])
        self.ipfs = ipfsapi.connect(
            self.ipfsConfig["host"],
            self.ipfsConfig["port"],
            self.ipfsConfig["protocol"])

    async def add_file(self, data: str):
        if data is None or data == "":
            raise ValueError("Data is None or invalid.")

        data_parsed = json.loads(data)
        result = await self.ipfs.add(
            json.dumps(data_parsed, separators=(',', ':')))

        return result["hash"]

    async def get_file(self, hash: str):
        if hash is None or hash == "":
            raise ValueError("Hash is None or invalid.")

        try:
            result = await self.ipfs.cat(hash)

            return result
        except ConnectionError as e:
            raise ConnectionError(
                e, "Connecting to the service has failed on the socket layer.")
        except ProtocolError as e:
            raise ProtocolError(
                e, "Parsing the response from the daemon failed. "
                "Is service on the remote end IPFS daemon?")
        except ErrorResponse as e:
            raise ErrorResponse(
                "Requested operation could not be carried out.", e)
        except StatusError as e:
            raise StatusError(e, "Daemon responded with an error.")
        except TimeoutError as e:
            raise TimeoutError(e, "Connection timeout error")
