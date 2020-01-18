from pymongo import MongoClient
from pprint import pprint
import datetime
from Task import Task
from User import User
from Cardlist import Cardlist
from GetList import ListGen

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
        link : str, 
        port: int=27017, 
        db_name : str="Deadline-bot"): #Пока данные захардкодил, хотя наверное можно подставлять (не проверял)
        self.port = port
        self.client = MongoClient("localhost", port)

        self.db = self.client[db_name] 
        self.users = self.db["Users"]
        self.tasks = self.db["Tasks"]
        self.card_lists = self.db["Cardlists"]


    def create(self, u : object): #Нужно как то переделать (работает) создает любой обьект в базе
        arg1 = str(u).find("<")
        arg2 = str(u).find(".")
        collection = self.db[str(u)[arg1 + 1:arg2] + "s"]
        collection.insert_one(u.__dict__)

    def add_user(self, user: User):
        self.users.insert_one(user.__dict__)

    def update(self): #Задумка
        pass

    def delete(self): #Задумка
        pass

    def get_all(self, name : str): #Задумка (работает) получить все из коллекции
        collection = self.db[name]
        a = collection.find({})
        
        return a

    def get_tasks(self, **kwars): #В отд. файл (еще пишу)
        pass
    
    def get_one(self, coll_name : str, query : dict, u : object = None): #Мб отредачить (работает) получить один обьект по коллекции по запросу (query)
        collection = self.db[coll_name]
        return(collection.find_one(query))

    def update_task(self, Name : str, t : Task): #Обновляет таск по названию, заменяет на модель (Мб нужно переделать)
        collection = self.db["Tasks"]
        collection.update_one({"Taskname" : Name}, {"$set" : t.__dict__})

    def delete_task(self, t : Task): #Удаляет таск по модели (мб нужно переделать)    
        collection = self.db["Tasks"]
        collection.delete_one(t.__dict__)

    def exists_in_db(self, tg_uid : int): #Артем попросил (работает) получение пользователя по id
        return self.users.find_one({"tg_uid" : tg_uid})

    def show_boards_assigner(self, tg_uid : int): #Доски по assigner'ам
        result = []
        collection = self.db["Cardlists"]
        cursor = collection.find({"tasks.Assigner" : tg_uid})
        for i in cursor:
            result.append(i)
        
        return(result)

    def show_boards_executor(self, tg_uid : int): #Доски по исполнителям
        result = []
        collection = self.db["Cardlists"]
        cursor = collection.find({"tasks.Executors" : tg_uid})
        for i in cursor:
            result.append(i)
        
        return(result)

    def get_task_tg_uid(self, tg_uid : int): #Таски по assigner'ам
        result = []
        collection = self.db["Tasks"]
        cursor = collection.find({"Assigner" : tg_uid})
        for i in cursor:
            result.append(i)
        return(result)
