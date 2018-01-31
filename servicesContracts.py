from typing import Any

from artifacts import *


def getServiceFromAddress(address: str) -> Any:
    """
    return the service of a corresponding currency contract address
    :param  address:
        The address of the currency contract
    """
    if not address:
        return None
    if isThisArtifact(requestEthereumArtifact, address):
        return RequestEthereumService()


def isThisArtifact(artifact, address: str) -> bool:
    """
    return True if any address in the network is sanitized address,
    otherwise it returns False
    :param  artifact:
        RequestNetwork Artifact to use in its interactions
        with the Ethereum network
    :param  address:
        The address of the currency contract
    """
    if not address:
        return False
    sanitizedAddress = address.lower()
    for network in artifact['networks'].values():
        if ('address' in network and
                network['address'].lower() == sanitizedAddress):
            return True
    return False
