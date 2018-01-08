from typing import Iterable
from copy import deepcopy

from time import Time

DAYS = set(('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'))

class Event:
    def __init__(self, name: str, days: Iterable[str], from_time: Time, to_time: Time, description=''):
        assert set(days).issubset(DAYS)
        assert from_time.in_seconds() <= to_time.in_seconds()

        self.name = name
        self.days = days
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

    # TODO: this method should implement the update method within the DAO and only handle updating the entity in the DB
    # using the DAO class
    # TODO: if you need to update a class variable in python it is simply done as Event.name = 'NEW NAME'
    def update(self, new_name=None, new_days=None, new_from_time=None, new_to_time=None, new_description=None):
        if new_name is not None:
            self.name = new_name
        if new_days is not None:
            self.days = new_days
        if new_from_time is not None:
            self.from_time = new_from_time
        if new_to_time is not None:
            self.to_time = new_to_time
        if new_description is not None:
            self.description = new_description

    def serialize(self):
        event_dict = deepcopy(vars(self))
        event_dict['from_time'] = vars(event_dict['from_time'])
        event_dict['to_time'] = vars(event_dict['to_time'])
        return event_dict