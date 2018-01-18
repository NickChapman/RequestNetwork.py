from json import load

class JSONLoader(dict):
    def __init__(self, filename):
        with open(filename) as f:
            super().__init__(load(f))