from typing import Any, Union

from artifacts import *

from servicesExtensions.requestSyncrhoneExtensionEscrow_service import RequestSynchroneExtensionEscrowService

def getServiceFromAddress(address: str) -> Union[RequestSynchroneExtensionEscrowService, None]:
    """
    Returns the service of a corresponding extension contract address
    :param address: The address of the extension contract
    :return: The service object or None if not found
    """
    pass

def isThisArtifact(artifact: Any, address: str) -> bool:
    """
    TODO: Fill out a description of what this does, no notes in RequestNetwork.js repo
    :param artifact:
    :param address:
    :return:
    """
    pass