import json
from flask import request
from flask_restful import Resource

from schedule import Schedule

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

class ScheduleAPI(Resource):
    # Return entire schedule with details info on events
    def get(self, owner):
        sched = Schedule.get(owner)
        return sched.serialize()

    # Add or remove an event to/from a schedule based on args
    def put(self, owner):
        data = read_args(request)
        if 'event_name' not in data:
            abort(404, message='"event_name" field is required to update shcedule')
        sched = Schedule.get(owner)
        if data['action'] == 'ADD':
            sched.add_event(data['event_name'])
        elif data['action'] == 'REMOVE':
            sched.remove_event(data['event_name'])
        else:
            abort(404, message='Invalid "action" field to update schedule')

        return sched.serialize(), 201
