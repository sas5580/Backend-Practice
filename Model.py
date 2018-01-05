from typing import Iterable, List, Dict
from copy import deepcopy

DAYS = set(('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'))

class Time:
    def __init__(self, hour: int, minute: int):
        assert 0 <= minute < 60 and 0 <= hour < 24
        self.hour = hour
        self.minute = minute

    @classmethod
    def fromdict(cls, time_dict: Dict[str, int]):
        return cls(time_dict['hour'], time_dict['minute'])

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

    @classmethod
    def fromdict(cls, event_dict):
        name = event_dict['name']
        days = event_dict['days']
        fromTime = Time.fromdict(event_dict['fromTime'])
        toTime = Time.fromdict(event_dict['toTime'])
        description = event_dict['description'] if 'description' in event_dict else ''
        return cls(name, days, fromTime, toTime, description)

    def serialize(self):
        event_dict = deepcopy(vars(self))
        event_dict['fromTime'] = vars(event_dict['fromTime'])
        event_dict['toTime'] = vars(event_dict['toTime'])
        return event_dict

class Schedule:
    def __init__(self, owner: str, events: List[Event]=[]):
        self.owner = owner
        self.events = events

    @classmethod
    def fromdict(cls, sched_dict):
        owner = sched_dict['owner']
        events = [Event.fromdict(e) for e in sched_dict['events']]
        return cls(owner, events)

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

    def serialize(self):
        sched_dict = {'owner': self.owner}
        sched_dict['events'] = [e.serialize() for e in self.events]
        return sched_dict

    def __getitem__(self, day: str):
        if day not in DAYS:
            raise KeyError('Schedule must be accessed with a day, received ' + day)
        day_events = (e for e in self.events if day in e.days)
        return sorted(day_events, key=lambda e: e.fromTime.inSeconds())

