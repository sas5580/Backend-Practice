from copy import deepcopy
from datetime import datetime, time

from eventdao import EventDAO

def read_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S').time()

class Event:
    dao = EventDAO()

    def __init__(self, document: dict):
        self.id = str(document['_id']) if '_id' in document else None
        self.name = document['name'] if 'name' in document else None
        self.days = document['days'] if 'days' in document else None
        self.from_time = document['from_time'] if 'from_time' in document else None
        self.to_time = document['to_time'] if 'to_time' in document else None
        self.description = document['description'] if 'description' in document else None

    @classmethod
    def exists(cls, e_id):
        return cls.dao.count_id(e_id) > 0:

    @classmethod
    def get(cls, event_name = None):
        event_dicts = cls.dao.get(event_name)
        if event_dicts is None:
            return None
        return [cls(e) for e in event_dicts]

    @classmethod
    def get_by_id(cls, id_str):
        event_dict = cls.dao.get_by_id(id_str)
        return cls(event_dict) if event_dict else None

    @classmethod
    def create(cls, event_dict):
        event = cls(event_dict)
        e_id = cls.dao.create(event)
        event.id = e_id
        return event

    def update(self, event_dict):
        for prop, val in event_dict.items():
            self.__dict__[prop] = val
        self.dao.update(self)
        return self

    @classmethod
    def delete(cls, e_id):
        return cls.dao.delete(e_id)
