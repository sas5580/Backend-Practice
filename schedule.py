from typing import Iterable
from flask_restful import abort

from scheduledao import ScheduleDAO
from event import Event

class Schedule:
    dao = ScheduleDAO()

    def __init__(self, document: dict):
        self.owner = document['owner'] if 'owner' in document else None
        self.events = set(document['events']) if 'events' in document else set()

    def serialize(self):
        sched_dict = {'owner': self.owner}
        sched_dict['events'] = [Event.get_by_id(e).serialize() for e in self.events]
        return sched_dict

    @classmethod
    def get(cls, owner):
        sched_dict = cls.dao.get(owner)
        print(sched_dict)
        if sched_dict is None:
            return None
        return cls(sched_dict)

    def add_event(self, event_name):
        e_id, event = Event.get(event_name)
        self.events.add(str(e_id))
        self.dao.update(self)
        return self

    def remove_event(self, event_name):
        e_id, event = Event.get(event_name)
        self.events.discard(str(e_id))
        self.dao.update(self)
        return self

