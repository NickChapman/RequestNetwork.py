import asyncio

from artifacts import *
from config import config
from servicesContracts.requestEthereum_service import RequestEthereumService
from servicesExtensions import getServiceFromAddress
from servicesExtensions.requestSyncrhoneExtensionEscrow_service import RequestSynchroneExtensionEscrowService
from servicesExternal.ipfs_service import Ipfs
from servicesExternal.web3_single import Web3Single

EMPTY_BYTES_32 = '0x0000000000000000000000000000000000000000'

class RequestCoreService:
    def __init__(self):
        self._web3Single = Web3Single.getInstance()
        self._ipfs = Ipfs.getInstance()
        self._abiRequestCore = requestCoreArtifact.abi
        if not requestCoreArtifact.networks[self._web3Single.networkName]:
            raise ValueError('RequestCore Artifact does not have configuration for network: "' + self._web3Single.networkName + '"')
        self._addressRequestCore = requestCoreArtifact.networks[self._web3Single.networkName].address
        self._instanceRequestCore = self._web3Single.web3.eth.Contract(self._abiRequestCore, self._addressRequestCore)

    async def getCurrentNumRequest(self):
        try:
            return self._instanceRequestCore.call().numRequests()
        except Exception as e:
            raise e

    async def getVersion(self):
        try:
            return self._instanceRequestCore.call().VERSION()
        except Exception as e:
            raise e

    def getCollectEstimation(self, expectedAmount: any, currencyContract: str, extension: str):
        pass

    async def getRequest(self, requestId: str):
        if not self._web3Single.isHexStrictBytes32(requestId):
            raise ValueError('requestId must be a 32 bytes hex string')
        try:
            data = self._instanceRequestCore.call().requests(requestId)
            if data.creator == EMPTY_BYTES_32:
                raise ValueError('request not found')

            # excluding BN
            dataResult = {
                'creator': data.creator,
                'currencyContract': data.currencyContract,
                'data': data.data,
                'extension': data.extension != EMPTY_BYTES_32 ? data.extension : None,
                'payee': data.payee,
                'payer': data.payer,
                'requestId': requestId,
                'state': int(data.state)
            }

            # get information from the currency contract
            if getServiceFromAddress(data.currencyContract):
                ccyContractDetails = await getServiceFromAddress(data.currencyContract).getRequestCurrencyContractInfo(requestId)
                dataResult['currencyContract'] = ccyContractDetails

            # get information from the extension contract
            if data.extension and data.extension != '' and getServiceFromAddress(data.extension):
                extensionDetails = await getServiceFromAddress(data.extension).getRequestExtensionInfo(requestId)
                dataResult['extension'] = extensionDetails

            # get ipfs details if needed
            if dataResult.data && dataResult.data != '':
                # might need to do some json wrangling
                dataResult['data'] = await self._ipfs.get_file(dataResult.data)
            else:
                dataResult['data'] = None

            return dataResult
        except Exception as e:
            raise e

    def getRequestByTransactionHash(self, hash:str):
        pass

    def getRequestEvents(self, requestId: str, fromBlock: int = None, toBlock: int = None):
        pass

    def getRequestsByAddress(self, address: str, fromBlock: int = None, toBlock: int = None):
        pass

    def getIpfsFile(self, hash: str):
        pass