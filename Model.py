from typing import Iterable

DAYS = set('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')

class Time:
    def __init__(self, hour: int, minute: int):
        assert 0 <= minute < 60 and 0 <= hour < 24
        self.hour = hour
        self.minute = minute

    def __repr__(self):
        return '%02d:%02d' % (self.hour, self.minute)

class Event:
    def __init__(self, name: str, days: Iterable[str], fromTime: Time, toTime: Time, description=''):
        assert set(days).issubset(DAYS)
        self.name = name
        self.days = days
        self.fromTime = fromTime
        self.toTime = toTime
        self.description = description

    def serialize(self):
        return vars(self)


class Schedule:
    def __init__(self, owner: str, events: List[Event]=[]):
        self.owner = owner
        self.events = events

    def addEvent(self, event: Event):
        self.events.append(event)

    def removeEvent(self, eventName: str):
        self.events = [e for e in self.events if e.name != eventName]

    def __getitem__(self, day):
        if day not in DAYS:
            raise KeyError('Schedule must be accessed with a day, received ', day)
        day_events = (e for e in self.events if day in e.days)
        return sorted(day_events, key=lambda e: e.fromTime.hour*60 + e.fromTime.minute)

