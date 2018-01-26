from typing import Any, Union

from artifacts import *
from servicesExtensions.requestSyncrhoneExtensionEscrow_service import RequestSynchroneExtensionEscrowService

def getServiceFromAddress(address: str) -> Union[RequestSynchroneExtensionEscrowService, None]:
    """
    Returns the service of a corresponding extension contract address
    :param  address:
        The address of the currency contract
    :return
        The service object or None if not found
    """
    if not address:
        return None
    if isThisArtifact(requestSynchroneExtensionEscrowArtifact, address):
        return RequestSynchroneExtensionEscrowService()

def isThisArtifact(artifact: Any, address: str) -> bool:
    """
    return True if any address in the network is sanitized address, otherwise it returns False
    :param  artifact:
        RequestNetwork Artifact to use in its interactions with the Ethereum network
    :param  address:
        The address of the currency contract
    """
    if not address:
        return False
    sanitizedAdress = address.lower()
    for network in artifact["networks"].values():
        if 'address' in network and network['address'].lower() == sanitizedAdress:
            return True
    return False