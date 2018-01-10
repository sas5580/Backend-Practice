import json
from flask import request
from flask_restful import Resource, abort

from schedule import Schedule

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

class ScheduleAPI(Resource):
    def get(self, owner):
        sched = Schedule.get(owner)
        if sched is None:
            abort(404, message='No schedule with owner {} exists'.format(owner))
        return vars(sched)

    def put(self, owner):
        data = read_args(request)

        sched = Schedule.get(owner)
        if sched is None:
            sched = Schedule({'owner': owner})

        if 'event_name' not in data:
            abort(404, message='"event_name" field is required to add event to shcedule')

        sched.add_event(data['event_name'])

        return vars(sched), 201

    def delete(self, owner):
        data = read_args(request)

        sched = Schedule.get(owner)
        if sched is None:
            abort(404, message='No schedule exists owned by {}'.format(owner))

        if 'event_name' not in data:
            abort(404, message='"event_name" field is required to remove event from shcedule')

        sched.remove_event(data['event_name'])

        return vars(sched), 204
