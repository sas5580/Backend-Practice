from typing import Iterable
from flask_restful import abort

from scheduledao import ScheduleDAO
from event import Event

class Schedule:
    dao = ScheduleDAO()

    def __init__(self, document: dict):
        self.owner = document['owner'] if 'owner' in document else None
        self.events = document['events'] if 'events' in document else []

    @classmethod
    def get(cls, owner):
        sched_dict = cls.dao.get(owner)
        if sched_dict is None:
            return None
        return cls(sched_dict)

    def add_event(self, event_name):
        e_id, event = Event.get(event_name)
        if e_id not in self.events:
            self.events.append(e_id)
        self.dao.update(self)
        return self

    def remove_event(self, event_name):
        e_id, event = Event.get(event_name)
        if e_id in self.events:
            self.events.remove(e_id)
        self.dao.update(self)
        return self

