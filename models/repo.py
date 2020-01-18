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
    def __init__(self, link : str, port : int, db_name : str): #Пока данные захардкодил, хотя наверное можно подставлять (не проверял)
        self.port = port
        self.client = MongoClient("localhost:27017") #Адрес сервера бд

        self.db = self.client["Deadline-bot"] #Название базы

    def create(self, u : object): #Нужно как то переделать (работает) создает любой обьект в базе
        arg1 = str(u).find("<")
        arg2 = str(u).find(".")
        collection = self.db[str(u)[arg1 + 1:arg2] + "s"]
        collection.insert_one(u.__dict__)

    def update(self): #Задумка
        pass

    def delete(self): #Задумка
        pass

    def get_all(self, name : str): #Задумка (работает) получить все из коллекции
        collection = self.db[name]
        a = collection.find({})
        for i in a:
            pprint(i)

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
        result = []
        collection = self.db["Users"]
        cursor = collection.find({"tg_uid" : tg_uid})
        for i in cursor:
            result.append(i)
        
        return(result)

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


b = Repo("localhost", 27017, "Database-bot")
print(b.get_task_tg_uid(1337))