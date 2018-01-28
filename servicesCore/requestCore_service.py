 import asyncio

from artifacts import *
from config import config
from servicesContracts.requestEthereum_service import RequestEthereumService
from servicesExtensions import getServiceFromAddress as getServiceExtensionFromAddress
from servicesContracts import getServiceFromAddress as getServiceContractFromAddress
from servicesExtensions.requestSyncrhoneExtensionEscrow_service import RequestSynchroneExtensionEscrowService
from servicesExternal.ipfs_service import Ipfs
from servicesExternal.web3_single import Web3Single

EMPTY_BYTES_32 = '0x0000000000000000000000000000000000000000'

class RequestCoreService:
    """
    The RequestCoreService class is the interface for the Request Core contract
    """

    def __init__(self):
        self._web3Single = Web3Single.getInstance()
        self._ipfs = Ipfs.getInstance()
        self._abiRequestCore = requestCoreArtifact['abi']
        if not requestCoreArtifact['networks'][self._web3Single.networkName]:
            raise ValueError('RequestCore Artifact does not have configuration for network: "' + self._web3Single.networkName + '"')
        self._addressRequestCore = requestCoreArtifact['networks'][self._web3Single.networkName]['address']
        self._instanceRequestCore = self._web3Single.web3.eth.Contract(self._abiRequestCore, self._addressRequestCore)

    async def getCurrentNumRequest(self):
        """
        Get the number of the last request (N.B. != id)
        """
        try:
            return self._instanceRequestCore.call().numRequests()
        except Exception as e:
            raise e

    async def getVersion(self):
        """
        Get the version of the contract
        """
        try:
            return self._instanceRequestCore.call().VERSION()
        except Exception as e:
            raise e

    async def getCollectEstimation(self, expectedAmount: any, currencyContract: str, extension: str):
        """
        Get the estimation of ether (in wei) needed to create a request
        :param expectedAmount: amount expected of the request
        :param currencyContract: address of the currency contract of the request
        :param extension: address of the extension contract of the request
        """
        if not self._web3Single.isAddressNoChecksum(currencyContract):
            raise ValueError('currencyContract must be a valid eth address')

        if extension and not self._web3Single.isAddressNoChecksum(extension):
            raise ValueError('extension must be a valid eth address')

        try:
            data = self._instanceRequestCore.call().getCollectEstimation(expectedAmount, currencyContract, extension)
            return data
        except Exception as e:
            raise e

    async def getRequest(self, requestId: str):
        """
        Get a request by its requestId
        :param requestId: requestId of the request
        """
        if not self._web3Single.isHexStrictBytes32(requestId):
            raise ValueError('requestId must be a 32 bytes hex string')
        try:
            data = self._instanceRequestCore.call().requests(requestId)
            if data.creator == EMPTY_BYTES_32:
                raise ValueError('request not found')

            # excluding BN
            dataResult = {
                'balance': data.balance,
                'creator': data.creator,
                'currencyContract': data.currencyContract,
                'data': data.data,
                'expectedAmount': data.expectedAmount,
                'extension': data.extension if data.extension != EMPTY_BYTES_32 else None,
                'payee': data.payee,
                'payer': data.payer,
                'requestId': requestId,
                'state': int(data.state)
            }

            # get information from the currency contract
            if getServiceContractFromAddress(data.currencyContract):
                ccyContractDetails = await getServiceContractFromAddress(data.currencyContract).getRequestCurrencyContractInfo(requestId)
                dataResult['currencyContract'] = ccyContractDetails

            # get information from the extension contract
            if data.extension and data.extension != '' and getServiceExtensionFromAddress(data.extension):
                extensionDetails = await getServiceExtensionFromAddress(data.extension).getRequestExtensionInfo(requestId)
                dataResult['extension'] = extensionDetails

            # get ipfs details if needed
            if dataResult.data and dataResult.data != '':
                # TODO: might need to do some json wrangling
                dataResult['data'] = await self._ipfs.get_file(dataResult.data)
            else:
                dataResult['data'] = None

            return dataResult
        except Exception as e:
            raise e

    async def getRequestByTransactionHash(self, hash: str):
        """
        Get a request and method called by the hash of a transaction
        :param hash: hash of the ethereum transaction
        """
        try:
            errors = []
            warnings = []
            transaction = await self._web3Single.getTransaction(_hash)
            if not transaction:
                raise ValueError('transaction not found')

            ccyContract = transaction.to

            ccyContractService = await servicesContracts.getServiceFromAddress(ccyContract)
            # get information from the currency contract
            if not ccyContractService:
                raise ValueError('Contract is not supported by request')

            method = ccyContractService.decodeInputData(transaction.input)
            if not method.name:
                raise ValueError('transaction data not parsable')

            request = None

            txReceipt = await self._web3Single.getTransactionReceipt(_hash)
            # if already mined
            if txReceipt:
                if txReceipt.status != '0x1' and txReceipt.status != 1:
                    errors.append('transaction has failed')
                elif transaction.method and transaction.method.pararmeters and transaction.method.parameters._requestId:
                    # simple action
                    request = await self.getRequest(transaction.method.parameters._requestId)
                elif transaction txReceipt.logs and txReceipt.logs[0] and self._web3Single.areSameAddressNoChecksum(txReceipt.logs[0]['address'], self._addressRequestCore)
                    # maybe a creation
                    event = self._web3Single.decodeTransactionLog(self._abiRequestCore, 'Created', txReceipt.logs[0])
                    if event:
                        request = self.getRequest(event.requestId)
            else:
                # if not mined
                methodGenerated = ccyContractService.generateWeb3Method(transaction.method.name, self._web3Single.resultToArray(transaction.method.parameters))
                options = {
                    'from': transaction.from,
                    'gas': transaction.gas,
                    'value': transaction.value
                }

                try:
                    test = await self._web3Single.callMethod(methodGenerated, options)
                except Exception as e:
                    warnings.append('transaction may have failed: ' + e)

                if transaction.gasPrice < config.ethereum.gasPriceMinimumCriticalInWei:
                    warnings.append('transaction gasPrice is low')

            errors = errors or None
            warnings = warnings or None
            return (request, transaction, errors, warnings)

        except Exception as e:
            raise e


    def getRequestEvents(self, requestId: str, fromBlock: int = None, toBlock: int = None):
        pass

    async def getRequestsByAddress(self, address: str, fromBlock: int = None, toBlock: int = None):
        """
        Get the list of requests connected to an address
        :param address: address to get the requests
        :param fromBlock: search requests from this block
        :param toBlock:  search requests until this block
        """
        try:
            networkName = self._web3Single.networkName

            # get events Created with payee == address
            eventsCorePayee = await self._instanceRequestCore.getPastEvents('Created', {
                'filter': {'payee': address},
                'fromBlock': fromBlock if fromBlock else requestCoreArtifact['networks'][networkName]['blockNumber'],
                'toBlock': toBlock if toBlock else 'latest'
            })

            # get events Created with payer == address
            eventsCorePayer = await this._instanceRequestCore.getPastEvents('Created', {
                'filter': {'payer': address},
                'fromBlock': fromBlock if fromBlock else requestCoreArtifact['network'][networkName]['blockNumber'],
                'toBlock': toBlock if toBlock else 'latest'
            })

            # clean the data and get timestamp for request as payee
            raise NotImplementedError('Still need to clean data')
            # TODO: implement this, I believe it is just adding 
            # a _meta dict to each event using a map

            # clean the data and get timestamp for request as payer
            # ditto here, but for eventsCorePayer

            return {'asPayee': eventsCorePayee, 'asPayer': eventsCorePayer}
        except Exception as e:
            raise e

    async def getIpfsFile(self, hash: str):
        """
        Get the file content from ipfs
        :param hash: hash of the file
        """
        return self._ipfs.get_file(hash)