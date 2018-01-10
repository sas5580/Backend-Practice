from typing import Iterable
from flask_restful import abort

from scheduledao import ScheduleDAO
from event import Event

class Schedule:
    dao = ScheduleDAO()

    def __init__(self, document: dict):
        self.id = str(document['_id']) if '_id' in document else None
        self.owner = document['owner'] if 'owner' in document else None
        self.events = document['events'] if 'events' in document else []

    @classmethod
    def get(cls, owner=None):
        sched_dicts = cls.dao.get(owner)
        if not isinstance(sched_dicts, list):
            return None
        return [cls(s) for s in sched_dicts]

    @classmethod
    def get_by_id(cls, s_id):
        sched_dict = cls.dao.get_by_id(s_id)
        return cls(sched_dict) if sched_dict else None

    @classmethod
    def create(cls, sched_dict):
        sched = cls(sched_dict)
        s_id = cls.dao.create(sched)
        sched.id = s_id
        return sched

    def add_event(self, e_id):
        if Event.exists(e_id) and e_id not in self.events:
            self.events.append(event.id)
            self.dao.update(self)
        return self

    def remove_event(self, e_id):
        if e_id in self.events:
            self.events.remove(event[0].id)
            self.dao.update(self)
        return self
