from Lib.pickleHandler import PickleHandler

class Stats:
    def __init__(self):
        self.pickleHandler = PickleHandler(self.config)

    def getStats(self):
        matches = self.pickleHandler.matches
        for match in matches:
            print(match.keys())