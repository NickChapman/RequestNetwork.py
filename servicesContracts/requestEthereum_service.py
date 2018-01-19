from typing import Any, List

from artifacts import *
from servicesCore.requestCore_service import RequestCoreService
from servicesExternal.ipfs_service import Ipfs
from servicesExternal.web3_single import Web3Single
from servicesExtensions import *


class RequestEthereumService:
    def __init__(self):
        pass

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
        pass

    def getRequestCurrencyContractInfo(self, requestId: str):
        pass

    def getRequest(self, requestId: str):
        pass

    def getRequestEvents(self, requestId: str, fromBlock: int = None, toBlock: int = None):
        pass

    def decodeInputData(self, data: Any) -> Any:
        pass

    def generateWeb3Method(self, name: str, parameters: List[Any]) -> Any:
        pass

    def getRequestEventsCurrencyContractInfo(self, requestId: str, fromBlock: int = None, toBlock: int = None):
        pass
