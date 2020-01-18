import telebot
from datetime import datetime
import config
import dbworker
import models
from models import User
from models import Task
from models import repo
from json import loads
import os
import webbrowser
from json import loads

from trello import TrelloApi

bot = telebot.TeleBot(config.token) 

#кнопки для тасков

create_task_markup = telebot.types.ReplyKeyboardMarkup(True)
create_task_markup.row('/add_task','/reset')

#кнопки для календаря

create_calendar_markup = telebot.types.ReplyKeyboardMarkup(True)
create_calendar_markup.row('/create_calendar')

#общие кнопки меню
markup = telebot.types.ReplyKeyboardMarkup(True)
markup.row('/start')

markup1 = telebot.types.ReplyKeyboardMarkup(True)
markup1.row('Мои доски', 'Мои задачи', 'Генератор Календаря')

markup2 = telebot.types.ReplyKeyboardMarkup(True)
markup2.row('Назад', 'Добавить задачу')

markup3 = telebot.types.ReplyKeyboardMarkup(True)
markup3.row('Мои доски', 'Мои задачи','Добавить задачу')

markup4 = telebot.types.ReplyKeyboardMarkup(True)
markup4.row('Назад', 'Добавить доску')

register_markup = telebot.types.ReplyKeyboardMarkup(True)
register_markup .row('/register','/register_reset')

@bot.message_handler(commands=["start"])
def get_text_messages(message):
    messagetext1 = "Привет"
    
    if message.text == "/start":
        r = repo.Repo("localhost", 27017, "Database-bot")
        if r.exists_in_db(int(message.from_user.id)) != None:
            bot.send_message(message.chat.id, messagetext1, reply_markup=markup1)
        else:
            bot.send_message(message.chat.id, "Зарегистрируйтесь", reply_markup=register_markup)
            
    elif message.text == "Мои доски":
        a = show_boards(int(message.from_user.id))
         #a = [{'_id': ObjectId('5e232c24d7d2efb90d939e8a'), 'cardlistname': 'test Cardlist', 'tasks': {'Name': 'testTask', 'Desc': 'descr', 'Due_date': datetime.datetime(2020, 1, 18, 18, 2, 44, 667000), 'Assigner': 1337, 'Executors': [228], 'Cardlist': []}}, {'_id': ObjectId('5e232c24d7d2efb90d939e8b'), 'cardlistname': 'test Cardlist1', 'tasks': {'Name': 'testTask', 'Desc': 'descr', 'Due_date': datetime.datetime(2020, 1, 18, 18, 2, 44, 667000), 'Assigner': 1337, 'Executors': [228], 'Cardlist': []}}, {'_id': ObjectId('5e232c24d7d2efb90d939e8c'), 'cardlistname': 'test Cardlist2', 'tasks': {'Name': 'testTask', 'Desc': 'descr', 'Due_date': datetime.datetime(2020, 1, 18, 18, 2, 44, 667000), 'Assigner': 1337, 'Executors': [228], 'Cardlist': []}}]
        #for i in range(a):
        #  i[3]
        bot.send_message(message.chat.id, "boards_list", reply_markup=markup4)
        #db
    elif message.text == "Мои задачи":
        #show_tasks(int(message.from_user.id))
        """
        tasks = [["sdfsdfsdfsdf", "dfgdfgdfgdfg",""]]
        self.Name = Name
        self.Desc = Desc
        self.Due_date = Due_date
        self.Assigner = Assigner
        self.Executors = Executors
        self.Cardlist = Cardlist
        for i in tasks
        """
       
        Desc = "description"
        #[#######....]
        deadline = datetime(2020, 2, 10, 4, 30)
        starttime  = datetime(2020, 1, 10, 4, 30) #базу поменять
        now = datetime.now()
        a = ((now - starttime)/(deadline-starttime))*10
        
        graphtime = "[_ _ _ _ _ _ _ _ _ _]"
        c = list(graphtime)
        for i in range(round(a)):
            print(round(a))
            c[i+1] = "##"
        graphtime = ''.join(c)  
        graphtime = f"{Desc} \n {graphtime}"
        bot.send_message(message.from_user.id, graphtime, reply_markup=markup2)
        #deadline = datetime.strptime("22/05/2017 12:30", "%d/%m/%Y %H:%M")
    elif message.text == "Генератор Календаря":
        bot.send_message(message.chat_id, "Жмите /create_calendar и следуйте указаниям", reply_markup=create_calendar_markup)
    elif message.text == "Добавить задачу":
        bot.send_message(message.chat_id, "Жмите /add_task и следуйте указаниям", reply_markup=create_task_markup)
    else:
        bot.send_message(message.chat.id, "введите /help для справки", reply_markup=markup1)



# Начало создания таска 
task_cr_name = ""
task_Desc = ""
task_due_dt = datetime.now()
@bot.message_handler(commands=["add_task"])
def add_task(message):
    bot.send_message(message.chat.id, "Введите название задачи")
    dbworker.set_state(message.chat.id, config.CreateTaskStates.S_ENTER_NAME.value)
@bot.message_handler(commands=["register_reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Ещё раз, введите название задания")
    dbworker.set_state(message.chat.id, config.CreateTaskStates.S_ENTER_NAME.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.CreateTaskStates.S_ENTER_NAME.value)
def task_entering_name(message):
    task_cr_name = message.text
    bot.send_message(message.chat.id, "Введите описание")
    dbworker.set_state(message.chat.id, config.CreateTaskStates.S_ENTER_DESC.value)   

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.CreateTaskStates.S_ENTER_DESC.value)
def task_entering_deadline_date(message):
        task_Desc = message.text
        bot.send_message(message.chat.id,"Выберите Дату Дедлайна") #подключить календарь либу
        dbworker.set_state(message.chat.id, config.CreateTaskStates.S_ENTER_Due_date.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.CreateTaskStates.S_ENTER_Due_date.value)
def task_entering_end(message):
        task_due_dt = message.text
        t = Task.Task(task_cr_name,task_Desc,task_due_dt, message.from_user.id, [],[],datetime.now())
        bot.send_message(message.chat.id,"Задача создана", reply_markup=markup1)
        r = repo.Repo("localhost", 27017, "Database-bot")
        r.create(t)
        dbworker.set_state(message.chat.id, config.CreateTaskStates.S_START.value)

# Создание таска
@bot.message_handler(commands=["add_task"])
def cmd_start(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.CreateTaskStates.S_ENTER_NAME.value:
        bot.send_message(message.chat.id, "Введите название задачи")
    elif state == config.CreateTaskStates.S_ENTER_DESC.value:
        bot.send_message(message.chat.id, "Введите описание")
    elif state == config.CreateTaskStates.S_ENTER_Due_date.value:
        bot.send_message(message.chat.id, "Введите дедлайн задачи")
    else:  # Под "остальным" понимаем состояние "0" 
        bot.send_message(message.chat.id, "Введите название задачи")
        dbworker.set_state(message.chat.id, config.CreateTaskStates.S_ENTER_NAME.value)


# регистрация 
usr_reg_name = ""
trello_reg_key = ""
@bot.message_handler(commands=["register"])
def add_name(message):
   
    bot.send_message(message.chat.id, "Введите имя")
    dbworker.set_state(message.chat.id, config.CreateUserStates.S_ENTER_NAME.value)

@bot.message_handler(commands=["register_reset"])
def cmd_usr_reset(message):
  
    bot.send_message(message.chat.id, "Ещё раз, введите имя")
    dbworker.set_state(message.chat.id, config.CreateUserStates.S_ENTER_NAME.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.CreateUserStates.S_ENTER_NAME.value)
def trello_entering(message):
    name = message.text
    url = trello_auth("url", name)
    bot.send_message(message.chat.id, f"Интеграция с Trello, перейдите по ссылке, скопируйте ключ, и вставьте в бота \n {url}")
    dbworker.set_state(message.chat.id, config.CreateUserStates.S_TRELLO_KEY.value) 

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.CreateUserStates.S_TRELLO_KEY.value)
def register_end(message):
        trello_key = message.text
        trello_auth("set_token", trello_key)
        #boards
        u = User.User(usr_reg_name,message.from_user.id,message.chat.id,trello_key )
        r = repo.Repo("localhost", 27017, "Database-bot")
        r.create(u)
        
        bot.send_message(message.chat.id,"Вы зарегистрированы", reply_markup=markup1)
        dbworker.set_state(message.chat.id, config.CreateUserStates.S_START.value)



"""
@bot.message_handler(commands=['calendar'])
def create_calendar(message):
    temp = []
    counter = 0
    for i in range(len(message.text)):
        if message.text[i] == "/n":
            temp.append(message.text[counter:i])
            counter = i
    e = event.Event(temp[0],temp[1],temp[2],temp[3])
   
    _ics = ics.ICS()
    _ics.add(e)
    print(_ics.to_bytes())
"""
    



def exists_in_db(userid):
    return True
def no_registered_board_user(message):
    no_registered_board_user(message.from_user.id)
 
    bot.send_message(message.from_user.id, "Create new board", reply_markup=markup3)

    return "sdf"

def trello_auth(action, parameter):
    with open(os.path.join(os.getcwd(), "config_.json"), "rb") as f:
        config_ = loads(f.read())

    with open(os.path.join(os.getcwd(), "config.json"), "rb") as f:
        config = loads(f.read())

    key = config_["trello"]["key"]  # '"093751fd307b96265f8f948a7afb540d"'
    secret = config_["trello"]["secret"]
    board_id = config_["trello"]["testBoard"]

    req_url = config["trello"]["requestURL"]
    acc_url = config["trello"]["accessURL"]
    auth_url = config["trello"]["authorizeURL"]
    my_token = config["trello"]["my_token"]


    trello = TrelloApi(key)

    # сгенерить ссыль для авторизации
    my_url = trello.get_token_url("Deadline Bot", expires="30days", write_access=True)
    if action == "url":
        return my_url
    elif action == "set_token":
        trello.set_token(parameter)


def show_boards(a):
    return True       
        
def default_procedure(message):
    print()

bot.polling(none_stop=True, interval=0)