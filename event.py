from copy import deepcopy
from datetime import datetime, time
from flask_restful import abort

from eventdao import EventDAO

def read_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S').time()

class Event:
    dao = EventDAO()

    def __init__(self, document: dict):
        self.name = document['name'] if 'name' in document else None
        self.days = document['days'] if 'days' in document else None
        self.from_time = document['from_time'] if 'from_time' in document else None
        self.to_time = document['to_time'] if 'to_time' in document else None
        self.description = document['description'] if 'description' in document else None

    @classmethod
    def get(cls, event_name):
        event_dict = cls.dao.get(event_name)
        if event_dict is None:
            abort(404, message='Event {} not found'.format(event_name))
        return str(event_dict['_id']), cls(event_dict)

    @classmethod
    def get_by_id(cls, id_str):
        event_dict = cls.dao.get_by_id(id_str)
        if event_dict is None:
            abort(404, message='Event with id "{}" not found'.format(id_str))
        return cls(event_dict)

    @classmethod
    def create(cls, event_dict):
        event = cls(event_dict)
        cls.dao.create(event)
        return event

    def update(self, event_dict):
        for prop, val in event_dict.items():
            self.__dict__[prop] = val

        self.dao.update(self)

        return self

    @classmethod
    def delete(cls, event_name):
        cls.dao.delete(event_name)
