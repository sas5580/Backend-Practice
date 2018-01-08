from typing import Iterable

from event import Event

class Schedule:
    def __init__(self, owner: str, events: Iterable[Event]=[]):
        self.owner = owner
        self.events = set(events)

    @classmethod
    def fromdict(cls, sched_dict):
        owner = sched_dict['owner']
        events = [Event.fromdict(e) for e in sched_dict['events']]
        return cls(owner, events)

    def addEvent(self, event: Event):
        self.events.add(event)

    def removeEvent(self, eventName: str):
        self.events.remove(eventName)

    def serialize(self):
        sched_dict = {'owner': self.owner}
        sched_dict['events'] = [e.serialize() for e in self.events]
        return sched_dict

    def __getitem__(self, day: str):
        if day not in DAYS:
            raise KeyError('Schedule must be accessed with a day, received {}'.format(day))
        day_events = (e for e in self.events if day in e.days)
        return sorted(day_events, key=lambda e: e.from_time.in_seconds())

