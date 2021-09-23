from typing import Set
import requests
import time
import logging
from riotwatcher import LolWatcher, ApiError

request_count = 0

def decorate_request(func):
    def inner(*args,**kwargs):
        global request_count
        if request_count % 50 == 0:
            print("making api request #" + str(request_count))
        logging.info("making api request #" + str(request_count))
        try:
            request_count += 1
            resp = func(*args, **kwargs)
            return resp
        except ApiError as err:
            if err.response.status_code == 429:
                retry_after = err.response.headers['Retry-After']
                print("waiting " + str(retry_after) + " seconds...")
                logging.info("waiting %s seconds...", str(retry_after))
                time.sleep(int(retry_after)+1)
                return func(*args, **kwargs)
            elif err.response.status_code == 504:
                print("waiting 3 seconds...")
                logging.info("waiting %s seconds...", str(3))
                time.sleep(3)
                logging.debug("got 504 error")
                return func(*args, **kwargs)
            else:
                logging.debug("got error: %s response: args: %s with kwargs: %s", err, args, *kwargs)
                raise
    return inner

class RiotAPIRequest:
    """
    specific api calls for riot's api
    """    
    def __init__(self, api_key, my_region):
        self.lol_watcher = LolWatcher(api_key)
        self.my_region = my_region
        
    @decorate_request
    def getAccountData(self, accountID):
        return self.lol_watcher.summoner.by_id(self.my_region, accountID)
    
    @decorate_request
    def getMatchData(self, gameId):
        return self.lol_watcher.match.by_id(self.my_region, gameId)
    
    @decorate_request
    def getRankedSeason11Games(self, accountId, beginIndex, queue = set(["420"])):
        """
        get matchlist for ranked season 11 only
        """
        resp = self.lol_watcher.match.matchlist_by_account(self.my_region, accountId, begin_index=beginIndex, queue=queue)
        return resp

    @decorate_request
    def getChallengerAccounts(self):
        return self.lol_watcher.league.challenger_by_queue(self.my_region, "RANKED_SOLO_5x5")

    @decorate_request
    def getGrandmasterAccounts(self):
        return self.lol_watcher.league.grandmaster_by_queue(self.my_region, "RANKED_SOLO_5x5")
        
    @decorate_request
    def getMasterAccounts(self):
        return self.lol_watcher.league.masters_by_queue(self.my_region, "RANKED_SOLO_5x5")