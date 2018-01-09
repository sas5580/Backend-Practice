from typing import Iterable
from flask_restful import abort

from scheduledao import ScheduleDAO
from event import Event

class Schedule:
    dao = ScheduleDAO()

    def __init__(self, owner: str, events: Iterable[Event]=[]):
        self.owner = owner
        self.events = set(events)

    @classmethod
    def fromdict(cls, sched_dict):
        owner = sched_dict['owner']
        events = [Event.get(e) for e in sched_dict['events']]
        return cls(owner, events)

    def add_event(self, event):
        self.events.add(event)

    def remove_event(self, event_name):
        self.events = {e for e in self.events if e.name != event_name}

    def serialize(self):
        sched_dict = {'owner': self.owner}
        sched_dict['events'] = [e.serialize() for e in self.events]
        return sched_dict

    def __getitem__(self, day: str):
        if day not in DAYS:
            raise KeyError('Schedule must be accessed with a day, received {}'.format(day))
        day_events = (e for e in self.events if day in e.days)
        return sorted(day_events, key=lambda e: e.from_time.in_seconds())

    @classmethod
    def get(cls, owner):
        sched_dict = cls.dao.get(owner)
        if sched_dict is None:
            abort(404, message='No schedule exists for {}'.format(owner))
        return cls.fromdict(sched_dict)

    def update(self, event_name, action):
        if action == 'ADD':
            event = Event.get(event_name)
            self.add_event(event)
        elif action == 'REMOVE':
            self.remove_event(event_name)
        else:
            abort(404, message='Invalid action "{}"'.format(action))
        self.dao.update(self)
        return self

