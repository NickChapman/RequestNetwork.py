from json import load


class JSONLoader(dict):
    """
    Used to load and interact with config files
    """
    def __init__(self, filename):
        with open(filename) as f:
            super().__init__(load(f))
