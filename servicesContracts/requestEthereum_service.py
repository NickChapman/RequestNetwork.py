from typing import Any, List

from artifacts import *
from servicesCore.requestCore_service import RequestCoreService
from servicesExternal.ipfs_service import Ipfs
from servicesExternal.web3_single import Web3Single
from servicesExtensions import *


class RequestEthereumService:
    def __init__(self):
        self.__web3Single = Web3Single.getInstance()
        self._ipfs = Ipfs.getInstance()
        self._abiRequestCore = requestCoreArtifact.abi
        self._requestCoreServices = new RequestCoreService()
        self._abiRequestEthereum = RequestEthereumArtifact.abi
        if (!requestEthereumArtifact.networks[self.__web3Single.networkName]) {
                    raiseException('RequestEthereum Artifact: no config for network : "' + self.__web3Single.networkName + '"')
                }
        self._addressRequestEthereum = requestEthereumArtifact.networks[self.__web3Single.networkName].address
        self._instanceRequestEthereum = new self.__web3Single.web3.eth.Contract(self._abiRequestEthereum,
            self._addressRequestEthereum)

    def createRequestAsPayee(self,
                             payer: str,
                             amountInitial: Any,
                             data: str = None,
                             extension: str = None,
                             extensionParams: str = None,
                             options: Any = None):
        pass

    def accept(self, requestId: str, options: Any = None):
        pass

    def cancel(self, requestId: str, options: Any = None):
        pass

    def paymentAction(self, requestId: str, amount: Any, additionals: Any, options: Any = None):
        pass

    def refundAction(self, requestId: str, amount: Any, options: Any = None):
        pass

    def subtractAction(self, requestId: str, amount: Any, options: Any = None):
        pass

    def additionalAction(self, requestId: str, amount: Any, options: Any = None):
        

    def getRequestCurrencyContractInfo(self, requestId: str):
        pass

    def getRequest(self, requestId: str):
        return self._requestCoreServices.getRequest(requestId)

    def getRequestEvents(self, requestId: str, fromBlock: int = None, toBlock: int = None):
        return self._requestCoreServices.getRequestEvents(requestId,fromBlock,toBlock)

    def decodeInputData(self, data: Any) -> Any:
        return self.__web3Single.decodeInputData(self._abiRequestEthereum, data)

    def generateWeb3Method(self, name: str, parameters: List[Any]) -> Any:
        return self.__web3Single.generateWeb3Method(self._instanceRequestEthereum, name, parameters)

    def getRequestEventsCurrencyContractInfo(self, requestId: str, fromBlock: int = None, toBlock: int = None):
        pass
