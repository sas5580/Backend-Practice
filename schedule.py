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
        event = Event.get_by_name(event_name)
        if event.id not in self.events:
            self.events.append(event.id)
        self.dao.update(self)
        return self

    def remove_event(self, event_name):
        event = Event.get_by_name(event_name)
        if event.id in self.events:
            self.events.remove(event.id)
        self.dao.update(self)
        return self
