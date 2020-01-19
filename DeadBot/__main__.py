import telebot
from datetime import datetime
from .config import CalendarStates, CreateTaskStates, CreateUserStates
from . import config
from . import dbworker
from ics import ics
from ics import event
import models
from models.User import User
from models.Task import Task
from models.repo import Repo
from json import loads
import os
import webbrowser
from json import loads

from trello import TrelloApi

bot = telebot.TeleBot(config.token) 
r = Repo("localhost", 27017, "Database-bot")

#kalendar var-s
state_calndar = 0
_ics = None
event_info_calendar = []


#кнопки для тасков

create_task_markup = telebot.types.ReplyKeyboardMarkup(True)
create_task_markup.row('/add_task','/reset')

#кнопки для календаря

markup = telebot.types.ReplyKeyboardMarkup(True)
markup.row('/calendar')

markup_calendar = telebot.types.ReplyKeyboardMarkup(True)
markup_calendar.row('/add_event', '/delete_all_events')

markup_reset_calendar = telebot.types.ReplyKeyboardMarkup(True)
markup_reset_calendar.row('/reset_calendar')


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
def start_point(message):
    if message.text == "/start":
        
        if r.exists_in_db(int(message.from_user.id)) != None:
            bot.send_message(message.chat.id, "Привет, это дедлайн треккер", reply_markup=markup1)
        else:
            bot.send_message(message.chat.id, "Зарегистрируйтесь", reply_markup=register_markup)
   
@bot.message_handler(commands=["my_boards"])
def get_boards(message):
    a = show_boards(int(message.from_user.id))
    #a = [{'_id': ObjectId('5e232c24d7d2efb90d939e8a'), 'cardlistname': 'test Cardlist', 'tasks': {'Name': 'testTask', 'Desc': 'descr', 'Due_date': datetime.datetime(2020, 1, 18, 18, 2, 44, 667000), 'Assigner': 1337, 'Executors': [228], 'Cardlist': []}}, {'_id': ObjectId('5e232c24d7d2efb90d939e8b'), 'cardlistname': 'test Cardlist1', 'tasks': {'Name': 'testTask', 'Desc': 'descr', 'Due_date': datetime.datetime(2020, 1, 18, 18, 2, 44, 667000), 'Assigner': 1337, 'Executors': [228], 'Cardlist': []}}, {'_id': ObjectId('5e232c24d7d2efb90d939e8c'), 'cardlistname': 'test Cardlist2', 'tasks': {'Name': 'testTask', 'Desc': 'descr', 'Due_date': datetime.datetime(2020, 1, 18, 18, 2, 44, 667000), 'Assigner': 1337, 'Executors': [228], 'Cardlist': []}}]
    #for i in range(a):
    #  i[3]
    bot.send_message(message.chat.id, "boards_list", reply_markup=markup4)
    #db
@bot.message_handler(commands=["my_tasks"])
def get_tasks(message):
    test_data = [{'_id': '5e2479892f43a9c99be960f5', 'Name': 'test1', 'Desc': 'test', 'Start_time': None, 'Due_date': datetime(2020, 1, 19, 17, 45, 13, 86000), 'Assigner': 123, 'Executors': [123], 'Cardlist': [123]},
            {'_id': '5e2479892f43a9c99be960f5', 'Name': 'test2', 'Desc': 'test', 'Start_time': None, 'Due_date': datetime(2020, 1, 19, 17, 45, 13, 86000), 'Assigner': 123, 'Executors': [123], 'Cardlist': [123]},
            {'_id': '5e2479892f43a9c99be960f5', 'Name': 'test3', 'Desc': 'test', 'Start_time': None, 'Due_date': datetime(2020, 1, 19, 17, 45, 13, 86000), 'Assigner': 123, 'Executors': [123], 'Cardlist': [123]},
            {'_id': '5e2479892f43a9c99be960f5', 'Name': 'test4', 'Desc': 'test', 'Start_time': None, 'Due_date': datetime(2020, 1, 19, 17, 45, 13, 86000), 'Assigner': 123, 'Executors': [123], 'Cardlist': [123]}]
        
    if test_data != None:
        #show_tasks(int(message.from_user.id))
        
        for i in range(len(test_data)):
            Name = test_data[i]['Name']
            starttime = test_data[i]['Start_time']
            deadline = test_data[i]['Due_date']
            #[#######....]
            #deadline = datetime(2020, 2, 10, 4, 30)
            starttime  = datetime(2020, 1, 10, 4, 30) #базу поменять
            now = datetime.now()
            a = ((now - starttime)/(deadline-starttime))*10
        
            graphtime = "[_ _ _ _ _ _ _ _ _ _]"
            c = list(graphtime)
            for i in range(round(a)):
                c[i+1] = "##"
            graphtime = ''.join(c)  
            graphtime = f"{Name} \n {graphtime}"
            bot.send_message(message.from_user.id, graphtime, reply_markup=markup2)
            #deadline = datetime.strptime("22/05/2017 12:30", "%d/%m/%Y %H:%M")
    else:
        bot.send_message(message.from_user.id, "у вас нет задач, создайте новую", reply_markup=markup2)    

# Начало создания таска 
task_cr_name = ""
task_Desc = ""
task_due_dt = datetime.now()
@bot.message_handler(commands=["add_task"])
def add_task(message):
    bot.send_message(message.chat.id, "Введите название задачи")
    dbworker.set_state(message.chat.id, config.CreateTaskStates.S_ENTER_NAME.value)
@bot.message_handler(commands=["task_reset"])
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
        t = Task(task_cr_name,task_Desc,task_due_dt, message.from_user.id, [],[],datetime.now())
        bot.send_message(message.chat.id,"Задача создана", reply_markup=markup1)
        r = Repo("localhost", 27017, "Database-bot")
        r.add_task(t)
        dbworker.set_state(message.chat.id, config.CreateTaskStates.S_START.value)

#Создание таска
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
    bot.send_message(message.chat.id, f"Интеграция с Trello, перейдите по ссылке, скопируйте токен, и вставьте в бота \n {url}")
    dbworker.set_state(message.chat.id, config.CreateUserStates.S_TRELLO_KEY.value) 

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.CreateUserStates.S_TRELLO_KEY.value)
def register_end(message):
        trello_key = message.text
        trello_auth("set_token", trello_key)
        #boards
        u = User(usr_reg_name,message.from_user.id,message.chat.id,trello_key )
        
        r.add_user(u)
        
        bot.send_message(message.chat.id,"Вы зарегистрированы", reply_markup=markup1)
        dbworker.set_state(message.chat.id, config.CreateUserStates.S_START.value)

#calendar
@bot.message_handler(commands=["reset_calendar"])
def cmd_reset_calendar(message):
    # Go back to first step for create event
    bot.send_message(message.chat.id, "Clear old data. Enter start time:", reply_markup=markup_reset_calendar)
    global state_calndar
    state_calndar = config.CalendarStates.S_START_TIME.value

@bot.message_handler(commands=["add_event"])
def add_new_event(message):
    # Add new event to calendar
    bot.send_message(message.chat.id, "Enter start time:", reply_markup=markup_reset_calendar)
    global state_calndar
    state_calndar = config.CalendarStates.S_START_TIME.value

@bot.message_handler(commands=["delete_all_events"])
def del_all_events(message):
    # Delete all events from calendar
    global _ics
    ics.ICS.delete_all(_ics)
    _ics = ics.ICS([])
    bot.send_message(message.chat.id, "All events have been removed")

@bot.message_handler(commands=["calendar"])
def cmd_calendar(message):
    global state_calndar
    if state_calndar == config.CalendarStates.S_START_TIME.value:
        bot.send_message(message.chat.id, "Waiting for start time")
    elif state_calndar == config.CalendarStates.S_DUE_TIME.value:
        bot.send_message(message.chat.id, "Waiting for due time")
    elif state_calndar == config.CalendarStates.S_SUMMARY.value:
        bot.send_message(message.chat.id, "Waiting for summary")
    elif state_calndar == config.CalendarStates.S_DESCRIPTION.value:
        bot.send_message(message.chat.id, "Waiting for description")
    else:  # Start position for event
        bot.send_message(message.chat.id, "Enter start time:", reply_markup=markup_reset_calendar)
        state_calndar = config.CalendarStates.S_START_TIME.value
        global _ics
        _ics = ics.ICS([])
        print(_ics)

@bot.message_handler(func=lambda message: state_calndar == config.CalendarStates.S_START_TIME.value) 
def event_start_time(message):
    # Se step for new event
    bot.send_message(message.chat.id, "Due time:")
    event_info_calendar.append(message.text)
    global state_calndar
    state_calndar = config.CalendarStates.S_DUE_TIME.value

@bot.message_handler(func=lambda message: state_calndar == config.CalendarStates.S_DUE_TIME.value) 
def event_due_time(message):
    # Second step for new event
    bot.send_message(message.chat.id, "Summary:")
    event_info_calendar.append(message.text)
    global state_calndar
    state_calndar = config.CalendarStates.S_SUMMARY.value

@bot.message_handler(func=lambda message: state_calndar == config.CalendarStates.S_SUMMARY.value) 
def event_summary(message):
    # Third step for new event
    bot.send_message(message.chat.id, "Description:")
    event_info_calendar.append(message.text)
    global state_calndar
    state_calndar = config.CalendarStates.S_DESCRIPTION.value

@bot.message_handler(func=lambda message: state_calndar == config.CalendarStates.S_DESCRIPTION.value) 
def event_description(message):
    # Fourth step for new event
    bot.send_message(message.chat.id, "Done!", reply_markup=markup_calendar)
    event_info_calendar.append(message.text)

    global state_calndar
    state_calndar = config.CalendarStates.S_START_TIME.value

    e = event.Event(event_info_calendar[0], event_info_calendar[1], event_info_calendar[2], event_info_calendar[3])
    event_info_calendar.clear()
    
    global _ics
    _ics.add(e)
    ics_bytes = _ics.to_bytes()
    f = open('file', 'wb')
    f.write(_ics.to_bytes())
    bot.send_message(message.chat.id, "Bytes: " + ics_bytes)
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
    
    key = "093751fd307b96265f8f948a7afb540d"
    
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