from math import floor
from typing import Any, Callable, List

from web3 import Web3 as WEB3

from config import config
from lib.etherum_abi_perso import toSolidityBytes32 as etherumToSolid


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        # not sure about should we use else or not
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls.__instance


class Web3Single(metaclass=Singleton):
    def __init__(self, web3Provider: Any = None, networkId: int = None):
        self.web3 = WEB3(web3Provider or new WEB3.providers.HttpProvider(
            config.ethereum.nodeUrlDefault
            [config.ethereum.default]))  # put here right link
        self.networkId = Web3Single.getNetworkName(networkId) if (
            networkId) else config.ethereum.default

    @staticmethod
    def getInstance():
        return new Web3Single()

    # We skip BN because it's useless in Python

    @staticmethod
    def getNetworkName(networkId: int) -> str:
        return {
            1: 'main',
            2: 'morden',
            3: 'ropsten',
            4: 'rinkeby',
            42: 'kovan'
        }.get(networkId, 'private')

    async def broadcastMethod(self,
                        method: Any,
                        callbackTranactionHash: Callable[[str], Any],
                        callbackTransactionReceipt: Callable[[Any], None],
                        callbackTransactionConfirmation: Callable[[int], Any],
                        callbackTransactionError: Callable[[Exception], Exception],
                        options: Any = None):
        '''
        Send a web3 method
        :param method: the method to send
        :param callbackTransactionHash: callback when the transaction is submitted
        :param callbackTransactionReceipt: callback when the transaction is mined (0 confirmation block)
        :param callbackTransactionConfirmation: callback when a new block is mined (up to 20)
        :param callbackTransactionError: callback when an error occured
        :param options: options for the method (gasPrice, gas, value, from)
        '''
        options['numberOfConfirmation'] = None
        if 'from' not in options:
            try:
                accounts = await self.web3.eth.getAccounts()
                options['from'] = accounts[0]
            except Exception as e:
                return callbackTransactionError(e)
        forcedGas = options['gas']
        options['value'] = options['value'] or 0
        options['gas'] = options['gas'] or 0
        options['gasPrice'] = options['gasPrice'] or self.web3.utils.toWei(config['ethereum']['gasPriceDefault'], config['ethereum']['gasPriceDefaultUnit'])
        # get the gas estimation
        try:
            estimatedGas = method.estimateGas(options)
            # it is safer to add 5% of gas
            options['gas'] = forcedGas if forcedGas else floor(estimatedGas * 1.05)
            # try the method offline
            try:
                # try the method offline
                method.call(options)
                # everything looks fine, let's send the transaction
                method.transact(options)
                    .on('transactionHash', callbackTranactionHash)
                    .on('receipt', callbackTransactionReceipt)
                    .on('confirmation', callbackTransactionConfirmation)
                    .on('error', callbackTransactionError)
            except:
                # try with more gas (*2)
                options['gas'] = forcedGas if forcedGas else floor(estimatedGas * 2)
                # try the method offline
                try:
                    method.call(options)
                    # everything looks fine, let's send the transaction
                    method.transact(options)
                    .on('transactionHash', callBackTransactionHash)
                    .on('receipt', callbackTransactionReceipt)
                    .on('confirmation', callbackTransactionConfirmation)
                    .on('error', callbackTransactionError)
                except Exception as e2:
                    return callbackTransactionError(e2)
        except Exception as e:
            return callbackTransactionError(e)
 
    async def callMethod(self, method: Any, options: Any = None):
        '''
        Send a web3 method
        :param method: the method to call()
        :param options: options for the method (gasPrice, gas, value, from)
        '''
        try:
            method.estimateGas(options)
            return method.call(options)
        except Exception as e:
            raise e

    async def getDefaultAccount(self):
        '''
        Get the default account (account[0] of the wallet)
        '''
        try:
            accs = self.web3.eth.getAccounts()
            if not accs:
                raise ValueError('No accounts found')
            return accs[0]
        except Exception as e:
            raise e

    def getDefaultAccountCallback(self, callback) -> None:
        '''
        Get the default account (account[0] of the wallet) with a callback
        '''
        try:
            accs = self.web3.eth.getAccounts()
            if len(accs) is 0:
                return callback(ValueError('No accounts found'), None)
            return callback(None, accs[0])
        except Exception as e:
            return callback(e, None)

    def toSolidityBytes32(self, type: str, value) -> Any:
        '''
        Convert a value in solidity bytes32 string
        :param type: type of the value to convert (e.g: address, unint, int, etc...)
        :param value: value to convert
        '''
        return self.web3.utils.encoding.to_hex(toSolidityBytes32(type, value))

    def arrayToBytes32(self, array, length: int) -> List[Any]:
        '''
        Convert an array to an array in solidity bytes32 string
        TODO: only support addresses so far
        :param array: array to convert
        :param length: length of the final array
        '''
        array = arrray or []
        ret = []
        for o in array:
            ret.append(self.web3.utils.encoding.to_hex(toSolidityBytes32('address', 0)))
        # fill the empty case with zeroes
        for i in range(len(array), length):
            ret.append(self.web3.utils.encoding.to_hex(toSolidityBytes32('bytes32', 0)))
        return ret

    def isAddressNoChecksum(self, address: str) -> bool:
        '''
        Check if an address is valid (ignoring case)
        :param address: address to check
        '''
        if not address:
            return False
        return self.web3.utils.isAddress(address.toLowerCase())

    def areSameAddressesNoChecksum(self, address1: str, address2: str) -> bool:
        '''
        Check if two addresses are equals (ignoring case)
        :param address1: address to check
        :param address2: address to check
        '''
        if not address1 or not address2 :
            return False
        return address1.toLowerCase() == address2.toLowerCase()

    def isHexStrictBytes32(self, hex: str) -> bool:
        '''
        Check if a string is a hex byte
        :param hex: string to check
        '''
        return self.web3.utils.isHexStrict(hex) and hex.length == 66

    def generateWeb3Method(self, contractInstance,
                           name: str,
                           parameters: List[Any]) -> Any:
        '''
        Generate web3 method
        :param contractInstance: contract instance
        :param name: method's name
        :param parameters: method's parameters
        '''
        return contractInstance.methods[name].apply(None, parameters)

    def decodeInputData(self, abi: List[Any], data: str) -> Any:
        '''
        Decode transaction input data
        :param abi: abi of the contract
        :param data: input data
        '''
        if not data:
            return {}

        method = {}
        for o in abi:
            if o['type'] == 'function':
                sign = o['name'] + '(' + ','.join(o['inputs']) + ')'
                encoded = self.web3.eth.abi.encodeFunctionSignature(sign)
                if encoded == data[:10]:
                    method = {'signature': sign, 'abi': o}
                    break

        if not method['signature']:
            return {}

        onlyParameters = '0x' + data[10]
        try:
            return {
                'name': method['abi']['name'],
                'parameters': self.web3.eth.abi.decodeParameters(method['abi']['inputs'], onlyParameters)
            }
        except:
            return {}

    def decodeTransactionLog(self, abi: List[Any], event: str, log: Any) -> Any:
        '''
        Decode transaction log parameters
        :param abi: abi of the contract
        :param event: event name
        :param log: log to decode
        '''
        eventInput : Any
        signature : str = ''
        # check here for some function no idea
        for o in abi:
            if o.name == event:
                eventInput = o.inputs
                signature = o.signature
                break
        if log.topics[0] != signature:
            return None
        return self.web3.eth.abi.decodelog(
            eventInput, log.data, log.topics[1:])

    def decodeEvent(self, abi: List[Any], eventName: str, event: Any) -> Any:
        '''
        Decode transaction event parameters
        :param abi: abi of the contract
        :param eventName: event name
        :param event: event to decode
        '''
        eventInput : Any
        for o in abi:
            if o.name == event:
                eventInput = o.inputs
                signature = o.signature
                break
        return self.web3.eth.abi.decodelog(
            eventInput, event.raw.data, event.topics[1:])

    def setUpOptions(self, options: Any) -> Any:
        '''
        Create or Clean options for a method
        :param options: options for the method (gasPrice, gas, value, from, numberOfConfirmation)
        '''
        if not options :
            options = {}
        if not options['numberOfConfirmation']:
            options['numberOfConfirmation'] = 0
        # BN is no here so i used different method check
        if options['gasPrice']:
            options['asPrice'] = self.web3.eth.gasPrice
        if options['gas']:
            options['gas'] = self.web3.eth.gas
        return options

    async def getTransactionReceipt(self, hash: str):
        '''
        Get Transaction receipt
        :param hash: transaction hash
        '''
        return self.web3.eth.getTransactionReceipt(hash)

    async def getTransaction(self, hash: str):
        '''
        Get Transaction
        :param hash: transaction hash
        '''
        return self.web3.eth.getTransaction(hash)

    async def getBlockTimestamp(self, blockNumber: int):
        '''
        Get timestamp of a block
        :param blockNumber: number of the block
        '''
        try:
            if not self._blockTimestamp['blockNumber']:
                block = await self.web3.eth.getBlock(blockNumber)
                if not block:
                    raise ValueError('Block {} not found'.format(blockNumber))
                self._blockTimestamp['blockNumber'] = block['timestamp']
        except Exception as e:
            raise e

    def resultToArray(self, obj: Any) -> List[Any]:
        result: List[Any] = List[]
        for i in range(len(obj)):
            result.append(obj[i])
        return result
