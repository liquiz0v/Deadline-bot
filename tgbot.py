import telebot
import ics
from ics import event
from datetime import datetime
import config
import dbworker

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

@bot.message_handler(commands=["start"])
def get_text_messages(message):
    messagetext1 = "Привет"
    
    if message.text == "/start":
         if exists_in_db(int(message.from_user.id)) != None:
             bot.send_message(message.chat.id, messagetext1, reply_markup=markup1)
            
         else:
             trello_and_add_tg_auth(message)
             

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
@bot.message_handler(commands=["add_task"])
def add_task(message):
    bot.send_message(message.chat.id, "Введите название задачи")
    dbworker.set_state(message.chat.id, config.CreateTaskStates.S_ENTER_NAME.value)
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Ещё раз, введите название задания")
    dbworker.set_state(message.chat.id, config.CreateTaskStates.S_ENTER_NAME.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.CreateTaskStates.S_ENTER_NAME.value)
def task_entering_name(message):
    bot.send_message(message.chat.id, "Введите описание")
    dbworker.set_state(message.chat.id, config.CreateTaskStates.S_ENTER_DESC.value)   

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.CreateTaskStates.S_ENTER_DESC.value)
def task_entering_deadline_date(message):
        bot.send_message(message.chat.id,"Выберите Дату Дедлайна") #подключить календарь либу
        dbworker.set_state(message.chat.id, config.CreateTaskStates.S_ENTER_Due_date.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.CreateTaskStates.S_ENTER_Due_date.value)
def task_entering_end(message):
        bot.send_message(message.chat.id,"Задача создана", reply_markup=markup1)
         
        #dbworker.set_state(message.chat.id, config.CreateTaskStates.S_ENTER_Due_date.value)

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

def trello_and_add_tg_auth(message):
    bot.send_message(message.from_user.id,"...", reply_markup=markup2)

def show_boards(a):
    return True       
        
def default_procedure(message):
    print()

bot.polling(none_stop=True, interval=0)