from typing import Any, List

from artifacts import *
from servicesCore.requestCore_service import RequestCoreService
from servicesExtensions import *
from servicesExternal.ipfs_service import Ipfs
from servicesExternal.web3_single import Web3Single


class RequestEthereumService:
    def __init__(self):
        self._web3Single = Web3Single.getInstance()
        self._ipfs = Ipfs.getInstance()
        self._abiRequestCore = requestCoreArtifact.abi
        self._requestCoreServices = new RequestCoreService()
        self._abiRequestEthereum = RequestEthereumArtifact.abi

        if not requestEthereumArtifact.networks[self.__web3Single.networkName]:
            raise ValueError(
                'RequestEthereum Artifact: no config for network : "' +
                self._web3Single.networkName + '"')

        self._addressRequestEthereum = (
            requestEthereumArtifact.networks
            [self.__web3Single.networkName].address)

        self._instanceRequestEthereum = self._web3Single.web3.eth.Contract(
            self._abiRequestEthereum,
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

    def paymentAction(self, requestId: str, amount: Any,
                      additionals: Any, options: Any = None):
        pass

    def refundAction(self, requestId: str, amount: Any, options: Any = None):
        pass

    def subtractAction(self, requestId: str, amount: Any, options: Any = None):
        pass

    def additionalAction(self, requestId: str, amount: Any, 
                         options: Any = None):
        pass

    def getRequestCurrencyContractInfo(self, requestId: str):
        pass

    def getRequest(self, requestId: str):
        return self._requestCoreServices.getRequest(requestId)

    def getRequestEvents(self, requestId: str, fromBlock: int = None,
                         toBlock: int = None):
        return self._requestCoreServices.getRequestEvents(
            requestId, fromBlock, toBlock)

    def decodeInputData(self, data: Any) -> Any:
        return self._web3Single.decodeInputData(self._abiRequestEthereum, data)

    def generateWeb3Method(self, name: str, parameters: List[Any]) -> Any:
        return self._web3Single.generateWeb3Method(
            self._instanceRequestEthereum, name, parameters)

    def getRequestEventsCurrencyContractInfo(self, requestId: str,
                                             fromBlock: int = None, 
                                             toBlock: int = None):
        pass
