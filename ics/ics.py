"""
Example:

BEGIN:VCALENDAR
PRODID:-//ostrogoth//
VERSION:2.0
BEGIN:VEVENT
DTSTART:20200118T111500
DTEND:20200118T130000
DTSTAMP:20200118T111500
UID:b883ea9b-0ea2-4f04-b444-88164aa732d4@b883.org
DESCRIPTION:Generate iCalendar before hackathon ends
SUMMARY:Generate Calendar
END:VEVENT
END:VCALENDAR

"""

from typing import List, Dict
import io

from .event import Event


class ICS:
    def __init__(self, events: List[Event] = None):
        """
        events - list of events
        """
        self.events: List[Event] = events

    def __str__(self):
        begin = "BEGIN:VCALENDAR\nPRODID:-//ostrogoth//\nVERSION:2.0\n"
        end = "END:VCALENDAR\n"
        string = ""
        string += begin

        for e in self.events:
            string += str(e)

        string += end

        return string

    def add(self, event: Event) -> bool:
        try:
            self.events.append(Event)
            return True
        except Exception:
            return False

    def delete(self, **kwargs: Dict[str, str]):
        """
        remove event from calendar with filter
        """
        for e in list(self.events):
            dt = list(e.__dict__.keys())
            for key in list(e.__dict__.keys()):
                if key in list(kwargs.keys()):
                    if e.__dict__[key] == kwargs[key]:
                        self.events.remove(e)
                        continue

    def delete_all(self):
        """ delete all event objects from event list """
        self.events = None

    def to_bytes(self) -> bytes:
        """
        returns byte array.\n
        with open('file.ics', 'rb') as f:
        \tf.write(calendar_object.to_bytes())
        """

        return bytes(str(self), encoding="utf-8")
