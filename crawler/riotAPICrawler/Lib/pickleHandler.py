import os
import pickle

class PickleHandler:
    """
    handle pickle file IO
    """
    data = None
    matches = None
    count = None

    def __init__(self, config):
        self.__config = config 
        self.__dataPath = os.path.join(os.path.dirname(os.path.dirname(__file__)),"Data",self.__config.dataPickleFile)
        self.__matchesPath = os.path.join(os.path.dirname(os.path.dirname(__file__)),"Data",self.__config.matchesPickleFile)
        self.__pickleFiles = [self.__dataPath]
        self.__checkFilesExist()
        self.read_data()
        self.read_matches()
    
    def __checkFilesExist(self):
        for f in self.__pickleFiles:
            if not os.path.isfile(f):
                with (open(f, "wb")) as openfile:
                    try:
                        pickle.dump({'accounts':{}},openfile)
                    except:
                        print("failed to write new pickle file: {} for accounts".format(f))

    def read_data(self):
        """
        read accountData
        """
        if self.data:
            print("accountsData already exists")
        else:
            with (open(self.__dataPath, "rb")) as openfile:
                self.data = pickle.load(openfile)

    def write_data(self):
        """
        write accountData
        """
        with (open(self.__dataPath, "wb")) as openfile:
            try:
                pickle.dump(self.data, openfile)
            except:
                print("error writing pickle output for accounts")
    
    def read_matches(self):
        """
        read matches
        """
        if self.matches:
            print("matchesData already exists")
        else:
            try:
                with (open(self.__matchesPath, "rb")) as openfile:
                    self.matches = pickle.load(openfile)
            except:
                print("failed to read matches")
                self.matches = {}

    def write_matches(self):
        """
        write matches
        """
        with (open(self.__matchesPath, "wb")) as openfile:
            try:
                pickle.dump(self.matches, openfile)
            except:
                print("error writing pickle output for matches")
    
    def pickleSeparator(self):
        a = self.data['accounts']
        accounts = {}
        for k in a.keys():
            accounts[a[k]["accountId"]] = {k:v for k,v in a[k].items() if k != 'matchList' and k != 'accountId'}
        matchLists = {}
        matches = {}
        matchqueue = {}
        count = 0
        count2 = 0
        count3 = 0
        for k in a.keys():
            if 'matchList' in a[k].keys():
                for match in a[k]['matchList']:
                    l = []
                    lm = len(a[k]['matchList'])
                    m = {k:v for k,v in match.items() if k != 'matchData'}
                    l.append(m)
                    if 'matchData' in match.keys(): 
                        matches[match['gameId']] = {k:v for k,v in match['matchData'].items() if k != 'gameId'}
                        count2 += 1
                    else:
                        matchqueue[match['gameId']] = {k:v for k,v in m.items() if k != 'gameId'}
                        count3 += 1
                    matchLists[a[k]["accountId"]] = [l]
                    count += 1

        with open('accounts.pickle', 'wb') as f:
            pickle.dump(accounts, f)

        with open('matchLists.pickle', 'wb') as f:
            pickle.dump(matchLists, f)

        with open('matches.pickle', 'wb') as f:
            pickle.dump(matches, f)

        with open('matchqueue.pickle', 'wb') as f:
            pickle.dump(matchqueue, f)