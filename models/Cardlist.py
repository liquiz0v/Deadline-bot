from typing import List


from .User import User

class Cardlist:
    def __init__(self, cardlistname : str, tasks : List[User]):
        self.cardlistname = cardlistname
        self.tasks = tasks
