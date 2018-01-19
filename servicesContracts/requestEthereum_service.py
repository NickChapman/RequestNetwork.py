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
                             **kwargs):
        pass

    def accept(self, requestId: str, **kwargs):
        pass

    def cancel(self, requestId: str, **kwargs):
        pass

    def paymentAction(self, requestId: str, amount: Any, additionals: Any, **kwargs):
        pass

    def refundAction(self, requestId: str, amount: Any, **kwargs):
        pass

    def subtractAction(self, requestId: str, amount: Any, **kwargs):
        pass

    def additionalAction(self, requestId: str, amount: Any, **kwargs):
        pass

    def getRequestCurrencyContractInfo(self, requestId: str):
        pass

    def getRequest(self, requestId: str, **kwargs):
        pass

    def decodeInputData(self, data: Any) -> Any:
        pass

    def generateWeb3Method(self, name: str, parameters: List[Any]) -> Any:
        pass

    def getRequestEventsCurrencyContractInfo(self, requestId: str, **kwargs):
        pass
