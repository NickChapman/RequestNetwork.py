from typing import Any, List
from web3 import Web3 as WEB3

from config import config
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        #not sure about should we use else or not
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls.__instance


class Web3Single(metaclass = Singleton):
    def __init__(self, web3Provider: Any = None, networkId: int = None):
        self.web3 = WEB3(web3Provider or new WEB3.providers.HttpProvider(config.ethereum.nodeUrlDefault[config.ethereum.default])) #put here right link
        self.networkId = Web3Single.getNetworkName(networkId) if networkId  else config.ethereum.default

    @staticmethod
    def getInstance():
        return new Web3Single()

    # We skip BN because it's useless in Python

    @staticmethod
    def getNetworkName(networkId: int ) -> str:
        return {1 : 'main', 2 :'morden', 3 : 'ropsten', 4 : 'rinkeby', 42 :'kovan','default' : 'private'}.get(networkId,'default')

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
        if not address :
            return False
        return address and self.web3.utils.isAddress(address.toLowerCase())

    def areSameAddressesNoChecksum(self, address1: str, address2: str) -> bool:
        if not address1 or not address2 :
            return False
        return address1.toLowerCase() == address2.toLowerCase()

    def isHexStrictBytes32(self, hex: str) -> bool:
        return self.web3.utils.isHexStrict(hex) and hex.length == 66

    def generateWeb3Method(self, contractInstance,
                           name: str,
                           parameters: List[Any]) -> Any:
        return contractInstance.methods[name].apply(None, parameters)

    def decodeInputData(self, abi: List[Any], data: str) -> Any:
        pass

    def decodeTransactionLog(self, abi: List[Any], event: str, log: Any) -> Any:
        eventInput : Any
        signature : str = ''
        #check here for some function no idea
        for o in abi:
            if o.name == event:
                eventInput = o.inputs
                signature = o.signature
                break
        if log.topics[0] != signature :
            return None
        return self.web3.eth.abi.decodelog(eventInput, log.data, log.topics[1:])


    def decodeEvent(self, abi: List[Any], eventName: str, event: Any) -> Any:
        eventInput : Any
        for o in abi:
            if o.name == event:
                eventInput = o.inputs
                signature = o.signature
                break
        return self.web3.eth.abi.decodelog(eventInput, event.raw.data, event.topics[1:])

    def setUpOptions(self, options: Any) -> Any:
        if not options :
            options = {}
        if not options['numberOfConfirmation'] :
            options['numberOfConfirmation'] = 0
        #BN is no here so i used different method check
        if options['gasPrice'] :
            options['asPrice'] = self.web3.eth.gasPrice
        if options['gas'] :
            options['gas'] = self.web3.eth.gas
        return options

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
        result : List[Any] = List[]
        for i in range(len(obj)) :
            result.append(obj[i])
        return result
