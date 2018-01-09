import json
from datetime import datetime
from flask import request
from flask_restful import Resource, abort

from event import Event, DAYS

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

def read_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S').time()

def validate_days(days):
    if not set(days).issubset(DAYS):
        raise ValueError('Invalid day string(s) in list')

class EventAPI(Resource):
    # Returns event details in JSON format
    def get(self, name):
        event = Event.get(name)
        return event.serialize()

    # Creates a new event based on args and name
    def post(self, name):
        event_dict = read_args(request)
        try:
            event_dict['name'] = name
            event_dict['from_time'] = read_time(event_dict['from_time'])
            event_dict['to_time'] = read_time(event_dict['to_time'])
            if event_dict['from_time'] > event_dict['to_time']:
                raise ValueError
            validate_days(event_dict['days'])
        except Exception as e:
            abort(404, message='Invalid payload to create event: {}'.format(e))
        event = Event.create(event_dict)
        return event.serialize(), 201

    # Update exisiting event based on args
    def put(self, name):
        event = Event.get(name)
        update_dict = read_args(request)

        try:
            if 'from_time' in update_dict:
                update_dict['from_time'] = read_time(update_dict['from_time'])
            if 'to_time' in update_dict:
                update_dict['to_time'] = read_time(update_dict['to_time'])
            if 'days' in update_dict:
                validate_days(update_dict['days'])
        except:
            abort(404, message='Invalid payload to update event')

        event.update(update_dict)
        return event.serialize(), 201

    # Deletes the named event
    def delete(self, name):
        Event.delete(name)
        return name, 204
