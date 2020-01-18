import datetime

class Task:
    def __init__(
        self, 
        Name : str, 
        Desc : str, 
        Due_date : datetime, 
        Assigner : int, 
        Executors : list, 
        Cardlist : list,
        Start_time: datetime=None
        ):
        self.Name = Name
        self.Desc = Desc
        self.Start_time = Start_time
        self.Due_date = Due_date
        self.Assigner = Assigner
        self.Executors = Executors
        self.Cardlist = Cardlist
