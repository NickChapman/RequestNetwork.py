from artifacts import *
from config import config
from servicesContracts.requestEthereum_service import RequestEthereumService
from servicesExtensions.requestSyncrhoneExtensionEscrow_service import RequestSynchroneExtensionEscrowService
from servicesExternal.ipfs_service import Ipfs
from servicesExternal.web3_single import Web3Single


class RequestCoreService:
    def __init__(self):
        self._web3Single = Web3Single.getInstance()
        self._ipfs = Ipfs.getInstance()
        self._abiRequestCore = requestCoreArtifact.abi
        if not requestCoreArtifact.networks[self._web3Single.networkName]:
            raise ValueError('RequestCore Artifact does not have configuration for network: "' + self._web3Single.networkName + '"')
        self._addressRequestCore = requestCoreArtifact.networks[self._web3Single.networkName].address
        self._instanceRequestCore = self._web3Single.web3.eth.Contract(self._abiRequestCore, self._addressRequestCore)

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