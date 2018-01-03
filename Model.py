from typing import Iterable, List
from copy import deepcopy

DAYS = set(('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'))

class Time:
    def __init__(self, hour: int, minute: int):
        assert 0 <= minute < 60 and 0 <= hour < 24
        self.hour = hour
        self.minute = minute

    def inSeconds(self):
        return self.hour*60 + self.minute

    def __str__(self):
        return '%02d:%02d' % (self.hour, self.minute)

class Event:
    def __init__(self, name: str, days: Iterable[str], fromTime: Time, toTime: Time, description=''):
        assert set(days).issubset(DAYS)
        assert fromTime.inSeconds() <= toTime.inSeconds()

        self.name = name
        self.days = days
        self.fromTime = fromTime
        self.toTime = toTime
        self.description = description

    def serialize(self):
        event_dict = deepcopy(vars(self))
        event_dict['fromTime'] = vars(event_dict['fromTime'])
        event_dict['toTime'] = vars(event_dict['toTime'])
        return event_dict

class Schedule:
    def __init__(self, owner: str, events: List[Event]=[]):
        self.owner = owner
        self.events = events

    def addEvent(self, event: Event):
        self.events.append(event)

    def removeEvent(self, eventName: str):
        self.events = [e for e in self.events if e.name != eventName]

    def updateEvent(self, eventName: str, newName=None, newDays=None, newFromTime=None, newToTime=None, newDescription=None):
        event = next(filter(lambda e: e.name == eventName, self.events))
        if newName is not None:
            event.name = newName
        if newDays is not None:
            event.days = newDays
        if newFromTime is not None:
            event.fromTime = newFromTime
        if newToTime is not None:
            event.toTime = newToTime
        if newDescription is not None:
            event.description = newDescription

    def __getitem__(self, day: str):
        if day not in DAYS:
            raise KeyError('Schedule must be accessed with a day, received ' + day)
        day_events = (e for e in self.events if day in e.days)
        return sorted(day_events, key=lambda e: e.fromTime.inSeconds())

