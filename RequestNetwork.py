class RequestNetwork:
    def __init__(self, useIpfsPublic=True, provider=None, networkId=None):
        """
        creates a RequestNetwork instance that provides the public interface to
        RequestNetwork.py

        :param useIpfsPublic:
            use public Ipfs if true, else the private one 
            specified in src/config.json
        :param provider:
            the Web3 instance one wishes RequestNetwork to use in
            its interactions with the Ethereum network
        :param networkId:
            the Ethereum network ID
        """
        if provider and not networkId:
            raise ValueError('if you give the provider you have to give the '
                             'networkId too')
        # Will assume that the Singletons are initialized in the typical way
        # not the "singleton.init(...)" like in the .ts source

        #Initializing Web3 & Ipfs wrapper singletons
        Web3Single(provider, networkId)
        Ipfs(useIpfsPublic)
        self.requestCoreService = RequestCoreService()
        self.requestEthereumService = RequestEthereumService()
        self.requestSynchroneExtensionEscrowService = \
            RequestSynchroneExtensionEscrowService()
