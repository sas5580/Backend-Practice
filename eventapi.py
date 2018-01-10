import json
from datetime import datetime
from flask import request
from flask_restful import Resource, abort

from event import Event
from eventvalidations import *

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

class EventAPI(Resource):
    def get(self, name):
        e_id, event = Event.get(name)
        return vars(event)

    def post(self, name):
        data = read_args(request)
        try:
            validate_times(data['from_time'], data['to_time'])
            validate_days(data['days'])
            data['name'] = name
            event = Event.create(data)
            return vars(event), 201

        except Exception as e:
            abort(404, message='Invalid payload to create event: {}'.format(e))

    def put(self, name):
        e_id, event = Event.get(name)
        data = read_args(request)
        try:
            if 'from_time' in data:
                read_time(data['from_time'])
            if 'to_time' in data:
                read_time(data['to_time'])
            if 'days' in data:
                validate_days(data['days'])
            event.update(data)
            validate_times(event.from_time, event.to_time)
            return vars(event), 201

        except Exception as e:
            abort(404, message='Invalid payload to update event: {}'.format(e))

    def delete(self, name):
        Event.delete(name)
        return name, 204
