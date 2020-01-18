from enum import Enum

token = "" 
db_file = "database.vdb"


class CreateTaskStates(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # 
    S_ENTER_NAME = "1"
    S_ENTER_DESC = "2"
    S_ENTER_Due_date = "3"