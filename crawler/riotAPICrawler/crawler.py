from Lib.config import Config
from Lib.riotAPIRequest import RiotAPIRequest
from Lib.staticData import StaticData
from Lib.sqlHandler import SqlHandler
import logging
import os

class Crawler:
    def __init__(self):
        self.config = Config()
        self.riotAPIRequest = RiotAPIRequest(self.config.api_key,self.config.my_region)
        self.sqlHandler = SqlHandler()
        self.staticData = StaticData()
        logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.dirname(__file__)), "Logs", "testing.log"), level=logging.DEBUG)


    def updateAccountsData(self, accounts):
        print('called updateAccountsData')
        count = 0
        entries = accounts
        if "entries" in accounts.keys():
            entries = accounts["entries"]
        for entry in entries:
            summonerId = entry["summonerId"]
            summonerName = entry["summonerName"]
            row = self.sqlHandler.checkAccountByIdOrName(summonerId,summonerName)
            if row:
                print("182838912838",row)
                if row[4] != summonerName:
                    self.sqlHandler.updateAccount_summonerName(summonerId,summonerName)
                continue
            print("getting new account data for summonerName: " + summonerName)
            newAccountData = {key:value for key,value in self.riotAPIRequest.getAccountData(summonerId).items() if value is not summonerName}
            self.sqlHandler.insertAccount(newAccountData['id'],newAccountData['accountId'],newAccountData['puuid'],newAccountData['name'])
            count += 1
            if count % 20 == 0:
                print("got ",count," new accounts")

    def getAccountsData(self):
        """
        gets (and updates) account data (summonerName and encryptedAccountId) for either challenger or custom username list
        """
        if not self.config.usernames:
            print("querying challenger account list")
            self.updateAccountsData(self.riotAPIRequest.getChallengerAccounts())
            # print("querying grandmaster account list")
            # self.updateAccountsData(self.riotAPIRequest.getGrandmasterAccounts())
            # print("querying master account list")
            # self.updateAccountsData(self.riotAPIRequest.getMasterAccounts())
        else:
            self.updateAccountsData(self.config.usernames)

    def getAllMatches(self, name, id, accountId, beginIndex):
        """
        gets all matches for 2021 ranked for a specific user
        """
        def insertEachGameId(matches):
            for match in matches:
                self.sqlHandler.insertGameIds(match['gameId'],match['platformId'],match['timestamp'])
        nextBeginIndex = beginIndex
        print("getting first set of matches for user: " + name)
        rankedGamesStart = self.riotAPIRequest.getRankedSeason11Games(accountId,beginIndex)
        insertEachGameId(rankedGamesStart['matches'])
        maxIndex = rankedGamesStart["totalGames"]
        self.sqlHandler.updateAccount_maxIndex(id,maxIndex)
        while maxIndex > nextBeginIndex:
            print("getting", nextBeginIndex, "of", maxIndex, "matches for user:", name)
            matchesData = self.riotAPIRequest.getRankedSeason11Games(accountId, beginIndex=nextBeginIndex)
            insertEachGameId(matchesData['matches'])
            nextBeginIndex = matchesData["endIndex"]
        return maxIndex

    # def initializeChampionData(self):
    #     self.staticData.get_championData()

    # def getAllMatches(self):
    #     """
    #     return all matches from all players
    #     """
    #     accountsWithMatches = {account: self.pickleHandler.data['accounts'][account] for account in self.pickleHandler.data['accounts'] if 'matchList' in self.pickleHandler.data['accounts'][account].keys() and len(self.pickleHandler.data['accounts'][account]['matchList']) > 0}
    #     matchList = {}
    #     for account, keys in accountsWithMatches.items():
    #         for match in keys['matchList']:
    #             matchTrimmed = {k:v for k,v in match.items() if k!='gameId'}
    #             matchList.update({match['gameId']:matchTrimmed})
    #     return matchList

    # def fixStatusAsAccount(self):
    #     delList = []
    #     # for account, data in self.pickleHandler.data['accounts'].items():
    #         if 'status' in data.keys():
    #             delList.append(account)
    #     for account in delList:
    #         # del self.pickleHandler.data['accounts'][account]
    #     print(len(delList))
    #     # self.pickleHandler.write_data()

    def initial_crawl(self, setting = 0):
        self.getAccountsData()
        if setting == 0:
            rows = self.sqlHandler.checkAccounts()
            for row in rows:
                (row_id,id,accountId,puuid,name,timestamp,beginIndex,maxIndex) = row
                newMatchesData = []
                if beginIndex == 0:
                    print("getting all matches for account: " + name)
                elif beginIndex < maxIndex:
                    print("getting new matches for account: " + name)
                else:
                    print("already have all matches for account: " + name)
                    continue
                beginIndex = self.getAllMatches(name,id,accountId,beginIndex)
                self.sqlHandler.updateAccount_beginIndex(id,beginIndex)
                self.sqlHandler.updateAccount_timestamp(id)
        # elif setting == 1:
        #     total = 0
        #     # for account, data in self.pickleHandler.data['accounts'].items():
        #         if 'matchList' in data.keys() and len(data['matchList']) > 0:
        #             count = 0
        #             for match in data['matchList']:
        #                 if 'matchData' not in match.keys():
        #                     if match['platformId'] == str(self.config.my_region).upper():
        #                         count += 1
        #                         print("getting match data for gameId: " + match['gameId'])
        #                         match['matchData'] = self.riotAPIRequest.getMatchData(match['gameId'])
        #                         if count % 10 == 0:
        #                             # self.pickleHandler.write_data()
        #             # self.pickleHandler.write_data()
        #             total += count
        #     print(total)

    # def addMatchesFromMatchLists(self):
    #     accounts = self.pickleHandler.data['accounts']
    #     matches = self.pickleHandler.matches
    #     print(len(matches.keys()))
    #     count = 0
    #     for key, value in accounts.items():
    #         for k, v in value.items():
    #             if k == "matchList" and len(v)>0:
    #                 for match in v:
    #                     if match["gameId"] in matches.keys():
    #                         continue
    #                     else:
    #                         data = { k:v for k,v in match.items() if k != "gameId"}
    #                         matches.update({match["gameId"]:data})
    #                         count += 1
    #                 if count % 20 == 0:
    #                     print("saving 20 matches of " + str(count))
    #                     # self.pickleHandler.write_matches()
    #     print("saving last matches")
    #     self.pickleHandler.write_matches()
        
    # def checkWinRates(self):
    #     # matches = self.pickleHandler.matches
    #     for key, value in matches.items():
    #         # for k, v in value['matchData']['participants'][0].items():
    #         #     print(k,v)
    #         #     input()
    #         # gameDuration = value['matchData']['gameDuration']
    #         # blueWon = value['matchData']['teams'][0]['win'] == 'Win'
    #         blueBans = value['matchData']['teams'][0]['bans']
    #         bluePicks = []
    #         for i in range(5):
    #             bluePick = {'championId':value['matchData']['participants'][i]['championId'],'pickTurn':i+1}
    #             bluePicks.append(bluePick)
    #         print(bluePicks)
    #         print(blueBans)
    #         # redBans = value['matchData']['teams'][1]['bans']
    #         input()

    def debug(self):
        row = self.sqlHandler.checkAccountByIdOrName(summonerName='DippyDan')
        print(row)
        # rows = self.sqlHandler.checkAccounts()
        # print(rows[-1])
        # for row in rows:
        #     print(row)
        #     input()

    def getMaxIndexes(self):
        #TODO get the max index for all accounts
        pass

if __name__ == "__main__":
    crawler = Crawler()

    #for debugging
    crawler.debug()

    # for parsing
    # crawler.addMatchesFromMatchLists()
    # crawler.checkWinRates()
    
    # for crawling
    # crawler.initial_crawl(0)
    # crawler.initial_crawl(1)
    
    # for separating
    # crawler.pickleSeparator()