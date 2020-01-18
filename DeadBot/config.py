from enum import Enum

token = "1038237138:AAGUuXh8ku1wVpCoZJFR6_TozbJbSYxUOQc" 
db_file = "database.vdb"


class CreateTaskStates(Enum):
  
    S_START = "0"  # 
    S_ENTER_NAME = "1"
    S_ENTER_DESC = "2"
    S_ENTER_Due_date = "3"

class CalendarStates(Enum):
   
    S_START_TIME = "0"  # Начало нового диалога
    S_DUE_TIME = "1"
    S_SUMMARY = "2"
    S_DESCRIPTION = "3"
class CreateUserStates(Enum):
    S_START = "0"
    S_ENTER_NAME = "1"
    S_TRELLO_KEY = "2"