from typing import Any, List
from web3 import Web3 as WEB3

from config import config


class Web3Single:
    def __init__(self, web3Provider: Any = None, networkId: int = None):
        pass

    @staticmethod
    def getInstance():
        pass

    # We skip BN because it's useless in Python

    @staticmethod
    def getNetworkName(networkId: int) -> str:
        pass

    # Async
    def broadcastMethod(self,
                        method: Any,
                        callbackTranactionHash,
                        callbackTransactionReceipt,
                        callbackTransactionConfirmation,
                        callbackTransactionError,
                        options: Any = None):
        pass

    def callMethod(self, method, options: Any = None):
        pass

    # Async
    def getDefaultAccount(self):
        pass

    # Async
    def getDefaultAccountCallback(self, callback) -> None:
        pass

    def toSolidityBytes32(self, type: str, value) -> Any:
        pass

    def arrayToBytes32(self, array, length: int) -> List[Any]:
        pass

    def isAddressNoChecksum(self, address: str) -> bool:
        pass

    def areSameAddressesNoChecksum(self, address1: str, address2: str) -> bool:
        pass

    def isHexStrictBytes32(self, hex: str) -> bool:
        pass

    def generateWeb3Method(self, contractInstance,
                           name: str,
                           parameters: List[Any]) -> Any:
        pass

    def decodeInputData(self, abi: Any, data: str) -> Any:
        pass

    def decodeTransactionLog(self, abi: List[Any], event: str, log: Any) -> Any:
        pass

    def decodeEvent(self, abi: List[Any], eventName: str, event: Any) -> Any:
        pass

    def setUpOptions(self, options: Any) -> Any:
        pass

    # Async
    def getTransactionReceipt(self, hash: str):
        pass

    # Async
    def getTransaction(self, hash: str):
        pass

    # Async
    def getBlockTimestamp(self, blockNumber: int):
        pass

    def resultToArray(self, obj: Any) -> List[Any]:
        pass
