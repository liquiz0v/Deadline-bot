from typing import List

class User:
    def __init__(
        self, 
        name : str, 
        tg_uid : int, 
        tg_chatid : int, 
        trello_key: str,
        boards: List[str] = None
        ):
        self.Username = name
        self.tg_uid = tg_uid
        self.tg_chatid = tg_chatid
        self.boards = boards
        self.trello_key = trello_key 