"""
Example:

BEGIN:VEVENT
DTSTART:20200118T111500
DTEND:20200118T130000
DTSTAMP:20200118T111500
UID:b883ea9b-0ea2-4f04-b444-88164aa732d4@b883.org
DESCRIPTION:Generate iCalendar before hackathon ends
SUMMARY:Generate Calendar
END:VEVENT

"""

from uuid import uuid4
from datetime import datetime

from .time_formatter import from_iso


class Event:
    def __init__(
        self,
        start_time: datetime,
        due_time: datetime,
        summary,
        description,
        assigner=None,
        executor=None,
        location=None,
    ):
        """
        obligatory:\n
            start_time, due_time - time interval for the event, provided in
            datetime.datetime() iso format,
            summary - title of the event,
            description - body of the event.
        optionaly:\n
            assigner - person, who assign the task,
            executor - the one, who has to deal with the task,
            location - place, where it is going to be held.
            provide latitude and longitude in string format if want to get
            integration with gmaps
        """

        self.start_time = start_time
        self.due_time = due_time
        self.summary = summary
        self.assigner = assigner
        self.executor = executor
        self.description = description
        self.location = location
        self.uid = uuid4()
        self.prodid = "-//ostrogoth//"

    def __str__(self):
        begin = "BEGIN:VEVENT"
        end = "END:VEVENT"
        string = ""

        string += begin + "\n"
        string += f"DTSTART:{from_iso(self.start_time)}\n"
        string += f"DTEND:{from_iso(self.due_time)}\n"
        string += f"DTSTAMP:{from_iso(self.start_time)}\n"
        string += f"UID:{str(self.uid)}\n"
        string += f"DESCRIPTION:{self.description}"
        if self.executor is not None:
            string += f", must be done by: {self.executor}"
        if self.assigner is not None:
            string += f", assigned by: {self.assigner}"
        string += "\n"
        string += f"SUMMARY:{self.summary}\n"
        string += end + "\n"

        return string
