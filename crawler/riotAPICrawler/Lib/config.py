from configparser import ConfigParser
import os

class Config:
    def __init__(self):
        self.__configFile = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.ini')
        self.__config = ConfigParser() 
        self.__config.read(self.__configFile)
        self.__readUserSettings()
        self.__readConfig()

    def __str__(self):
        return '{0} api_key: {1}\n{0} accounts data pickle file: {2}\n{0} usernames: {3}'.format(self.__class__.__name__,self.api_key,self.dataPickleFile,self.usernames)

    def __readUserSettings(self):
        self.api_key = self.__config['User Settings']['api_key']
        self.my_region = self.__config['User Settings']['my_region']
        self.usernames = (self.__config['User Settings']['usernames'].split(',') if "usernames" in self.__config['User Settings'].keys() else None)

    def __readConfig(self):
        config = self.__config['DEFAULT']
        self.dataPickleFile = config['dataPickleFile']
        self.matchesPickleFile = config['matchesPickleFile']