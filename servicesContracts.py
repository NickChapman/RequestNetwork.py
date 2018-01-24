from typing import Any
from servicesContracts.requestEthereum_service import RequestEthereumService

"""
  getServiceFromAddress return the service of a coresponding currency contract address
  :param  address:
        The address of the currency contract
"""
def getServiceFromAddress(address: str) -> Any:
    if not address:
        return None
    if isThisArtifact(Artifacts.requestEthereumArtifact, address):
        return RequestEthereumService()

"""
  isThisArtifact return
  :param  artifact:
      RequestNetwork Artifact to use in its interactions with the Ethereum network
    :param  address:
        The address of the currency contract
"""
def isThisArtifact(artifact, address: str) -> bool:
    if not address:
        return False
    sanitizedAdress = address.lower()
    # assume artifact.networks is a dictionary
    return any((value.address.lower() == sanitizedAdress if not value.address else False
                for key,value in artifact.networks.items()))