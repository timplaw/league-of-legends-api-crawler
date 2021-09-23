import sqlite3
import time

class SqlHandler:
    def __init__(self):
        self.con = sqlite3.connect('league.db')
        self.cur = self.con.cursor()
        # self.alterAccountsTable()
        # self.alterGameIdsTable()
        # self.constructAccountsTable()
        # self.constructGameIdsTable()
    
    def constructAccountsTable(self):
        self.cur.execute('''CREATE TABLE accounts (
            rowId INTEGER NOT NULL PRIMARY KEY,
            id varchar(48) NOT NULL UNIQUE,
            accountId varchar(48) NOT NULL UNIQUE,
            puuid varchar(48) NOT NULL UNIQUE,
            summonerName varchar(16) NOT NULL UNIQUE,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            beginIndex INTEGER DEFAULT 0,
            maxIndex INTEGER DEFAULT 0,
        );
        ''')

    def constructGameIdsTable(self):
        self.cur.execute('''CREATE TABLE gameids (
            gameId INTEGER NOT NULL PRIMARY KEY,
            platformId varchar(4) NOT NULL,
            timestamp TIMESTAMP NOT NULL
        );
        ''')

    def constructMatchesTable(self):
        self.cur.execute('''CREATE TABLE matches (
            gameId INTEGER NOT NULL PRIMARY KEY,
            platformId varchar(4) NOT NULL,
            timestamp TIMESTAMP NOT NULL,

        );
        ''')
    
    def alterAccountsTable(self):
        self.cur.execute("ALTER TABLE accounts RENAME COLUMN lastCrawl TO timestamp")
        # self.cur.execute("ALTER TABLE accounts ADD CONSTRAINT df_lastCrawl DEFAULT GETDATETIME() FOR lastCrawl")
        # self.cur.execute("ALTER TABLE accounts ADD COLUMN maxIndex INTEGER DEFAULT 0")

    def alterGameIdsTable(self):
        # self.cur.execute("ALTER TABLE gameids ADD COLUMN platformId varchar(4) NOT NULL")
        self.cur.execute("ALTER TABLE gameids ADD COLUMN timestamp TIMESTAMP")

    def insertAccount(self,summonerId,accountId,puuid,summonerName):
        self.cur.execute("INSERT INTO accounts (id,accountId,puuid,summonerName) VALUES (?,?,?,?)", (summonerId,accountId,puuid,summonerName))
        self.con.commit()

    def updateAccount_summonerName(self, id, summonerName):
        self.cur.execute("UPDATE accounts SET summonerName = ? WHERE id = ?", (summonerName,id))
        self.con.commit()

    def updateAccount_beginIndex(self, id, beginIndex):
        self.cur.execute("UPDATE accounts SET beginIndex = ? WHERE id = ?", (beginIndex,id))
        self.con.commit()

    def updateAccount_maxIndex(self, id, maxIndex):
        self.cur.execute("UPDATE accounts SET maxIndex = ? WHERE id = ?", (maxIndex,id))
        self.con.commit() 

    def updateAccount_timestamp(self, id):
        timestamp = int(str(time.time()).split('.')[0])
        print(timestamp,"updated timestamp")
        self.cur.execute("UPDATE accounts SET lastCrawl = ? WHERE id = ?", (timestamp,id))
        self.con.commit()  
    
    def checkAccountByIdOrName(self, summonerId = "", summonerName = ""):
        self.cur.execute("SELECT * FROM accounts WHERE (id=? OR summonerName=?)", (summonerId,summonerName))
        rows = self.cur.fetchone()
        return rows

    def checkAccounts(self):
        self.cur.execute("SELECT * FROM accounts")
        rows = self.cur.fetchall()
        return rows
    
    def checkGameId(self, gameId):
        self.cur.execute("SELECT * FROM gameids WHERE gameId=?", (gameId,))
        rows = self.cur.fetchone()
        return rows

    def insertGameIds(self, gameId, platformId, timestamp):
        row = self.checkGameId(gameId)
        if row:
            return
        self.cur.execute("INSERT INTO gameids (gameId, platformId, timestamp) VALUES (?,?,?)", (gameId, platformId, timestamp))
        self.con.commit()