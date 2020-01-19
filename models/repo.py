from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
import datetime
from .Task import Task
from .User import User
from .Cardlist import Cardlist
from .GetList import ListGen

"""
Pymongo-repo
Before using this library, you need to have models of identities.
Example of usage:
1) Create model object, for expamle User.
2) Create Repo object.
3) Use create, update, delete or get functions.

1) u = User("Oleg", 285469, 2689574)
2) r = Repo("localhost", 27017, "Database-bot")
3) r.create(u)
"""

class Repo:
    def __init__(
        self, 
        link : str = "localhost", 
        port: int = 27017, 
        db_name : str = "Deadline-bot"): 

        self.port = port
        self.client = MongoClient("localhost", port)

        self.db = self.client[db_name] 
        self.users = self.db["Users"]
        self.tasks = self.db["Tasks"]
        self.card_lists = self.db["Cardlists"]


    def add_task(self, task : Task):
        self.tasks.insert_one(task.__dict__) 

    def add_user(self, user: User):
        self.users.insert_one(user.__dict__)
    
    def add_task(self, task: Task):
        self.tasks.insert_one(task.__dict__)

    #def add_cardlist(self, cardlist: Cardlist):
    #    self.cardlist.insert_one(user.__dict__)

    def add_cardlist(self, cardlist : Cardlist):
        self.card_lists.insert_one(cardlist.__dict__)

    def get_all(self, name : str): #(работает) получить все из коллекции
        return self.db[name].find({})

    def get_task(self, task_id : ObjectId):
        return(self.tasks.find_one({"_id" : task_id}))
    
    def get_one(self, coll_name : str, query : dict, u : object = None): #Мб отредачить (работает) получить один обьект по коллекции по запросу (query)
        return(self.db[coll_name].find_one(query))

    def update_task(self, Name : str, t : Task): #Обновляет таск по названию, заменяет на модель 
        self.db["Tasks"].update_one({"Taskname" : Name}, {"$set" : t.__dict__})

    def delete_task(self, t : Task): #Удаляет таск по модели    
        self.db["Tasks"].delete_one(t.__dict__)

    def exists_in_db(self, tg_uid : int): #Артем попросил (работает) получение пользователя по id
        return self.users.find_one({"tg_uid" : tg_uid})

    def show_boards_assigner(self, tg_uid : int): #Доски по assigner'ам
        result = []
        cursor = self.db["Cardlists"].find({"tasks.Assigner" : tg_uid})
        for i in cursor:
            result.append(i)
        
        return(result)

    def show_boards_executor(self, tg_uid : int): #Доски по исполнителям
        result = []
        cursor = self.db["Cardlists"].find({"tasks.Executors" : tg_uid})
        for i in cursor:
            result.append(i)
        
        return(result)

    def get_task_tg_uid(self, tg_uid : int): #Таски по assigner'ам
        result = []
        cursor = self.db["Tasks"].find({"Assigner" : tg_uid})
        for i in cursor:
            result.append(i)
        return(result)
