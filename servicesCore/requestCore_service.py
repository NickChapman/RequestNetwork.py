from artifacts import *
from config import config
from servicesContracts.requestEthereum_service import RequestEthereumService
from servicesExtensions.requestSyncrhoneExtensionEscrow_service import RequestSynchroneExtensionEscrowService
from servicesExternal.ipfs_service import Ipfs
from servicesExternal.web3_single import Web3Single


class RequestCoreService:
    def __init__(self):
        pass

    def getCurrentNumRequest(self):
        pass

    def getVersion(self):
        pass

    def getCollectEstimation(self, expectedAmount: any, currencyContract: str, extension: str):
        pass

    def getRequest(self, requestId: str):
        pass

    def getRequestByTransactionHash(self, hash:str):
        pass

    def getRequestEvents(self, requestId: str, fromBlock: int = None, toBlock: int = None):
        pass

    def getRequestsByAddress(self, address: str, fromBlock: int = None, toBlock: int = None):
        pass

    def getIpfsFile(self, hash: str):
        pass