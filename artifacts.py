from os.path import dirname, join

from lib import JSONLoader

_dir = dirname(__file__)

_core_artifact_path = join(_dir, *["artifacts", "RequestCore.json"])
requestCoreArtifact = JSONLoader(_core_artifact_path)

_ethereum_artifact_path = join(_dir, *["artifacts", "RequestEthereum.json"])
requestEthereumArtifact = JSONLoader(_ethereum_artifact_path)

_synchrone_extension_escrow_artifact_path = join(
    _dir, *["artifacts", "RequestSynchroneExtensionEscrow.json"])
requestSynchroneExtensionEscrowArtifact = JSONLoader(
    _synchrone_extension_escrow_artifact_path)
