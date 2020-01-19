from enum import Enum

token = "1038237138:AAGUuXh8ku1wVpCoZJFR6_TozbJbSYxUOQc" 
db_file = "database.vdb"

class CalendarStates(Enum):
   
    S_START_TIME = "0"  # Начало нового диалога
    S_DUE_TIME = "1"
    S_SUMMARY = "2"
    S_DESCRIPTION = "3"
class CreateTaskStates(Enum):
  
    S_START = "4"  # 
    S_ENTER_NAME = "5"
    S_ENTER_DESC = "6"
    S_ENTER_Due_date = "7"


class CreateUserStates(Enum):
    S_START = "8"
    S_ENTER_NAME = "9"
    S_TRELLO_KEY = "10"