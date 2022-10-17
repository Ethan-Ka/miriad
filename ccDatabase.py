import os
import json
os.system("python -m pip install \"pymongo[srv]\"")
from pymongo import MongoClient
import pymongo


class cCoin:
    pass
    #creamCoin = dict()


class mongoDb():
    def __init__(self):
        self.url = "https://data.mongodb-api.com/app/data-fqmbw/endpoint/data/v1"
        
        self.passw = os.environ["MONGOPW"].strip()
        self.url = fr"mongodb+srv://miriad:{self.passw}@cluster0.ydvin7k.mongodb.net/?retryWrites=true&w=majority"
        self.myclient = pymongo.MongoClient(self.url)
        
        self.database = self.myclient["miriad"]
        self.database = self.database.miriad
    def get_db(self):
        results = self.database.find({"_id":"daba"})
        list = []
        for i in results:
          list.append(i)
        #dict = json.loads(list[0])
        dict = list[0]
        return json.loads(dict['"data"'])
        
    def add_db(self, database):
        false = False
        true = True
        database = {"_id":"daba", 'data':{"942477753536634962": {"624384023132635146": {"coins": 99, "disabled": false, "admin": true, "username": "thedankboi"}, "770239477749776414": {"coins": 100, "disabled": false, "admin": false, "username": "abbskbab"}, "737363673223266395": {"coins": 100, "disabled": false, "admin": false, "username": "lottie"}, "790703548161196052": {"coins": 100, "disabled": false, "admin": false, "username": "saveme"}}, "storage": {"leaderboard": "1017476925977022495"}}
        }
        self.database.insert_one(database)
    def update_db(self, database):
      database = json.loads(json.dumps(database))
      strings = json.dumps(database)
      self.database.update_one({"_id":"daba"}, {"$set": {'"data"':strings,} })




class ccDatabase():
    global databasePath
    databasePath = r"data.txt"

    def __init__(self):
        self.mongodb = mongoDb()

    def isAdmin(self, guild, id):
      guild = str(guild)
      id = str(id)
      if not creamCoin[guild][id]["admin"]:
        return False
      if creamCoin[guild][id]:
        return True
    def addTaxes(self, guild, amount):
      try:
        guild = str(guild)
        for key in creamCoin[str(guild)].keys():
          if not creamCoin[str(guild)][key]["disabled"]:
            print(key)
            balance = creamCoin[guild][key]["coins"] #add taxes
            creamCoin[guild][key]["coins"] = balance+amount
            self.pushCCDatabase()
        return True
      except Exception as e:
        return e
    def loadCCDatabase(self):
    # read the CreamCoin database
        
        global creamCoin
        creamCoin = self.mongodb.get_db()
        #(json.dumps(content))
        #print(json.dumps(creamCoin))
        
    def creamCoinReturn(self):
        return creamCoin
    def createGuild(self, guild):
        if not guild in creamCoin:
          creamCoin[guild] = {"hi"}
          print('good')
    def create_user(self, guild:any, user_id:any, disabled:bool, admin:bool, userName,author:any):
        if not creamCoin[guild][author]["admin"]==True:
              return "noperms"
        if not guild in creamCoin:
            creamCoin[guild] = {}
        if not user_id in creamCoin[guild]:
            creamCoin[guild][user_id] = {
                "coins":100,
                "disabled":disabled,
                "admin":admin,
                "username":userName
            }
            self.pushCCDatabase()
            #print(json.dumps(creamCoin))
            return True
        else:
            return False
    def getLeaderboard(self, guild):
        #for key in creamCoin[guild][key]["coins"]
  #create a list that has the value
  # {creamCoin[guild][key]:creamCoin[guild][key]["coins"]}
  # and sort them using .sort()
  # do this in ccDatabase.py and return the list
  # for every key, leaderboard spot 1 to end:
  #embed.add_field(place+"Name", coins)
      list = {}
      for key in creamCoin[guild].keys():
        value1 = str(key)
        value2 = int(creamCoin[guild][key]["coins"])
        list[value1] = value2
      return sorted(list, key=list.get, reverse=True)
    
    def deleteUser(self, guild:any, user_id:any, author:any):
        if not creamCoin[guild][author]["admin"]==True:
              return "noperms"
        if not guild in creamCoin:
          return "guildnotfound"
        if not user_id in creamCoin[guild]:
          return True
        else:
          del creamCoin[guild][user_id]
          self.pushCCDatabase()
          return True
    def resetAll(self, guild:any):
        if not guild in creamCoin:
            return "guildnotfound"
        else:
          for key in creamCoin[guild].keys():
            print(str(key))
            print(str(creamCoin[guild][key]["coins"]))
            creamCoin[guild][key]["coins"] = 0
            self.pushCCDatabase()
    def getUsername(self, guild:any, target:any):
      return creamCoin[str(guild)][str(target)]["username"]
    def setCoins(self, guild:any, target:any, amount:any, author:any):
        if not creamCoin[guild][author]["admin"]==True:
            return "noperms"
        if not target in creamCoin[guild]:
            #create new user
            return "targetnotfound"
        if bool(creamCoin[guild][target]["disabled"]) == True:
            return "disabled"
        else:
            creamCoin[guild][target]["coins"] = amount
            self.pushCCDatabase()
            return True

    def setDisabled(self, guild: any, target: any, disabled: bool, author:any):
        if not creamCoin[guild][author]["admin"]==True:
            return "noperms"
        if not target in creamCoin[guild]:
            return "targetnotfound"
        if not guild in creamCoin:
            return "guildnotfound"
        else:
            creamCoin[guild][target]["disabled"] = disabled
            self.pushCCDatabase()
            return True
        
    def setAdmin(self, guild: any, target: any, admin: bool, author:any):
        if not creamCoin[guild][author]["admin"]==True:
            return "noperms"
        if not target in creamCoin[guild]:
            return "targetnotfound"
        if not guild in creamCoin:
            return "guildnotfound"
        else:
            creamCoin[guild][target]["admin"] = admin
            self.pushCCDatabase()
            return True
    
    
    def transfer(self, author:str, amount:str, guild:str, target:str):
        #print(json.dumps(creamCoin))
        
        if not author in creamCoin[guild]:
            return "usernotfound"
        if not target in creamCoin[guild]:
            self.create_user()
            balance = creamCoin[guild][target]["coins"]
            try:
                creamCoin[guild][target]["coins"] = balance + amount
            except Exception as e:
                return "transfererror"
            creamCoin[guild][author]["coins"] = creamCoin[guild][author]["coins"] - amount
            self.pushCCDatabase()
            return True
        if amount > int(creamCoin[guild][author]["coins"]):  # user has insufficient funds
            return "insfunds"
        
        
        else: # user passes checks
            balance = creamCoin[guild][target]["coins"]
            try:
                creamCoin[guild][target]["coins"] = balance + amount
            except Exception as e:
                return "transfererror"
            creamCoin[guild][author]["coins"] = creamCoin[guild][author]["coins"] - amount
            self.pushCCDatabase()
            return True
    def seeCoins(self, guild:any,target:any):
        if target in creamCoin[guild]:
          balance = creamCoin[guild][target]["coins"]
          return balance
        else:
          return "targetnotfound"
    def pushCCDatabase(self):
        # push the CreamCoin database
        self.mongo.update_db(creamCoin)
    
        #mongodb stuff here
    

#toCreate = str(target)+{":\n\n'coins':100,\n\n'disabled':False\n\n"}
#creamCoin[str(guild)] = toCreate
#creamCoin[guild][target]["coins"] = amount
#pushCCDatabase()
