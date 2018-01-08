from typing import Iterable
from copy import deepcopy
from flask_restful import abort

from time import Time
from eventdao import EventDAO


DAYS = set(('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'))

class Event:
    dao = EventDAO()

    def __init__(self, name: str, days: Iterable[str], from_time: Time, to_time: Time, description=''):
        assert set(days).issubset(DAYS)
        assert from_time.in_seconds() <= to_time.in_seconds()

        self.name = name
        self.days = set(days)
        self.from_time = from_time
        self.to_time = to_time
        self.description = description

    @classmethod
    def fromdict(cls, event_dict):
        name = event_dict['name']
        days = event_dict['days']
        from_time = Time.fromdict(event_dict['from_time'])
        to_time = Time.fromdict(event_dict['to_time'])
        description = event_dict['description'] if 'description' in event_dict else ''
        return cls(name, days, from_time, to_time, description)

    def serialize(self):
        event_dict = deepcopy(vars(self))
        event_dict['from_time'] = vars(event_dict['from_time'])
        event_dict['to_time'] = vars(event_dict['to_time'])
        return event_dict

    @classmethod
    def get(cls, event_name):
        event_dict = dao.get(event_name)
        if event_dict is None:
            abort(404, message='Event {} not found'.format(event_name))
        return cls.fromdict(event_dict)

    @classmethod
    def create(cls, event_name, event_dict):
        try:
            event_dict['name'] = event_name
            event = cls.fromdict(event_dict)
            cls.dao.create(event)
            return event
        except KeyError:
            abort(404, message='Invalid args to create event')

    def update(self, event_dict):
        if 'days' in event_dict:
            if not set(event_dict['days']).issubset(DAYS):
               abort(404, message='Invalid day string in days')
            self.days = event_dict['days']

        if 'from_time' in event_dict:
            try:
                new_time = Time.fromdict(event_dict['from_time'])
                self.from_time = new_time
            except ValueError:
                abort(404, message='Invalid from time')

        if 'to_time' in event_dict:
            try:
                new_time = Time.fromdict(event_dict['to_time'])
                self.to_time = new_time
            except ValueError:
                abort(404, message='Invalid to time')

        if 'description' in event_dict:
            self.description = event_dict['description']

        self.dao.update(self)

        return self

    @classmethod
    def delete(cls, event_name):
        event = cls.get(event_name)
        cls.dao.delete(event_name)
        return event



        

