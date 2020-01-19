import vedis
from . import config

def get_current_state(user_id):
    with vedis.Vedis(config.db_file) as db:
        try:
            return db[user_id].decode() 
        except KeyError: 
            return config.CreateTaskStates.S_START.value  

def set_state(user_id, value):
    with vedis.Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            # хз как обработать
            return False