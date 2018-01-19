from typing import Any, List
from web3 import Web3 as WEB3

from artifacts import *
from config import config
from servicesCore.requestCore_service import RequestCoreService
from servicesExternal.web3_single import Web3Single


class RequestSynchroneExtensionEscrowService:
    def __init__(self):
        pass

    def parseParameters(self, extensionParams: List[Any]) -> Any:
        pass

    def releaseToPayeeAction(self, requestId: str, options: Any = None):
        pass

    def getRequest(self, requestId: str):
        pass

    def getRequestExtensionInfo(self, requestId: str):
        pass

    def getRequestEvents(self, requestId: str, fromBlock: int = None, toBlock: int = None):
        pass

    def getRequestEventsExtensionInfo(self, requestId: str, fromBlock: int = None, toBlock: int = None):
        pass

