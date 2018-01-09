from typing import Iterable
from flask_restful import abort

from scheduledao import ScheduleDAO
from event import Event

class Schedule:
    dao = ScheduleDAO()

    def __init__(self, document: dict):
        self.owner = document['owner'] if 'owner' in document else None
        self.events = set(document['events']) if 'events' in document else None

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
        sched_dict['events'] = [Event.get(e) for e in sched_dict['events']]
        print(sched_dict)
        if sched_dict is None:
            abort(404, message='No schedule exists for {}'.format(owner))
        return cls(sched_dict)

    def add_event(self, event_name):
        event = Event.get(event_name)
        self.events.add(event)
        self.dao.update(self)
        return self

    def remove_event(self, event_name):
        self.events = {e for e in self.events if e.name != event_name}
        self.dao.update(self)
        return self

