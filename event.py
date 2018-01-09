from copy import deepcopy
from datetime import datetime, time
from flask_restful import abort

from eventdao import EventDAO

DAYS = set(('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'))

def read_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S').time()

class Event:
    dao = EventDAO()

    def __init__(self, documnet: dict):

        self.name = documnet['name'] if 'name' in documnet else None
        self.days = documnet['days'] if 'days' in documnet else None
        self.from_time = documnet['from_time'] if 'from_time' in documnet else None
        self.to_time = documnet['to_time'] if 'to_time' in documnet else None
        self.description = documnet['description'] if 'description' in documnet else None

    def serialize(self):
        event_dict = deepcopy(self.__dict__)
        event_dict['from_time'] = event_dict['from_time'].isoformat()
        event_dict['to_time'] = event_dict['to_time'].isoformat()
        return event_dict

    @classmethod
    def get(cls, event_name):
        event_dict = cls.dao.get(event_name)
        if event_dict is None:
            abort(404, message='Event {} not found'.format(event_name))
        event_dict['from_time'] = read_time(event_dict['from_time'])
        event_dict['to_time'] = read_time(event_dict['to_time'])
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



        

