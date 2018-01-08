from typing import Iterable, List, Dict
from copy import deepcopy

DAYS = set(('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'))


# TODO: as stated within the APP .. there are multiple resource models within this file, they should be broken apart into
# their respective class name files (ie: time.py)
class Time:
    def __init__(self, hour: int, minute: int):
        assert 0 <= minute < 60 and 0 <= hour < 24
        self.hour = hour
        self.minute = minute

    @classmethod
    def fromdict(cls, time_dict: Dict[str, int]):
        return cls(time_dict['hour'], time_dict['minute'])

    def in_seconds(self):
        return self.hour*60 + self.minute

    def __str__(self):
        return '%02d:%02d' % (self.hour, self.minute)
    
# TODO: as stated within the APP .. there are multiple resource models within this file, they should be broken apart into
# their respective class name files (ie: event.py)
class Event:
    def __init__(self, name: str, days: Iterable[str], from_time: Time, to_time: Time, description=''):
        assert set(days).issubset(DAYS)
        assert from_time.in_seconds() <= to_time.in_seconds()

        self.name = name
        self.days = days
        self.from_time = from_time
        self.to_time = to_time
        self.description = description

    @classmethod
    def fromdict(cls, event_dict):
        name = event_dict['name']
        days = event_dict['days']
        from_time = Time.fromdict(event_dict['from_time'])
        to_time = Time.fromdict(event_dict['to_time'])
        description = event_dict['description'] if 'description' in event_dict else ''
        return cls(name, days, from_time, to_time, description)

    # TODO: this method should implement the update method within the DAO and only handle updating the entity in the DB
    # using the DAO class
    # TODO: if you need to update a class variable in python it is simply done as Event.name = 'NEW NAME'
    def update(self, new_name=None, new_days=None, new_from_time=None, new_to_time=None, new_description=None):
        if new_name is not None:
            self.name = new_name
        if new_days is not None:
            self.days = new_days
        if new_from_time is not None:
            self.from_time = new_from_time
        if new_to_time is not None:
            self.to_time = new_to_time
        if new_description is not None:
            self.description = new_description

    def serialize(self):
        event_dict = deepcopy(vars(self))
        event_dict['from_time'] = vars(event_dict['from_time'])
        event_dict['to_time'] = vars(event_dict['to_time'])
        return event_dict

# TODO: as stated within the app.. this is a different resources model and should exist within its own class file named
# schedule.py
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

    def serialize(self):
        sched_dict = {'owner': self.owner}
        sched_dict['events'] = [e.serialize() for e in self.events]
        return sched_dict

    def __getitem__(self, day: str):
        if day not in DAYS:
            raise KeyError('Schedule must be accessed with a day, received ' + day)
        day_events = (e for e in self.events if day in e.days)
        return sorted(day_events, key=lambda e: e.fromTime.in_seconds())

