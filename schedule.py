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

    @classmethod
    def add_event(cls, s_id, e_id):
        res = cls.dao.add_event(s_id, e_id)
        return e_id if res > 0 else None

    @classmethod
    def remove_event(cls, s_id, e_id):
        res = cls.dao.remove_event(s_id, e_id)
        if cls.dao.events_empty(s_id):
            print("WORKED?")
            cls.dao.delete(s_id)
        return e_id if res > 0 else None
