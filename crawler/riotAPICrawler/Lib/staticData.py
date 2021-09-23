import requests
import pickle
import os

class StaticData:
    championData = None
    __championsPickleFile = os.path.join(os.path.dirname(os.path.dirname(__file__)),"Data","Static","champion.pickle")

    def __init__(self, championNames=["Vi"]):
        self.__championNames = championNames

    def __basicDataDragonQuery(self):
        url = "http://ddragon.leagueoflegends.com/cdn/10.11.1/data/en_US/champion.json"
        resp = requests.get(url=url)
        return resp.json()

    def get_championData(self):
        """
        check if we have a champion data file else write new one
        """
        self.read_championData()
        staticData = self.__basicDataDragonQuery()
        self.championData = {champ:staticData["data"][champ] for champ in self.__championNames}
        with open(self.__championsPickleFile, "wb") as openfile:
            pickle.dump(self.championData, openfile)

    def read_championData(self):
        if not self.championData:
            try:
                with open(self.__championsPickleFile, "rb") as openfile:
                    self.championData = pickle.load(openfile)
            except:
                # write the blank file if their is none
                with open(self.__championsPickleFile, "wb") as openfile:
                    # TODO: complete this
                    pass

def main():
    staticData = StaticData()
    staticData.get_championData()
    staticData.read_championData()

if __name__ == "__main__":
    main()