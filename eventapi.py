import json
from datetime import datetime
from flask import request
from flask_restful import Resource, abort

from event import Event
from eventvalidations import *

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

class EventAPI(Resource):
    def get(self, e_id):
        event = Event.get_by_id(e_id)
        return vars(event)

    def put(self, e_id):
        event = Event.get_by_id(e_id)
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

    def delete(self, e_id):
        Event.delete(e_id)
        return e_id, 204

class EventsAPI(Resource):
    def post(self):
        data = read_args(request)
        try:
            validate_times(data['from_time'], data['to_time'])
            validate_days(data['days'])
            event = Event.create(data)
            return vars(event), 201
        except Exception as e:
            abort(404, message='Invalid payload to create event: {}'.format(e))

    def get(self):
        name = request.args.get('name', default=None)
        if name is None:
            events = Event.get_all()
            return [vars(e) for e in events]
        else:
            event = Event.get_by_name(name)
            return vars(event)
