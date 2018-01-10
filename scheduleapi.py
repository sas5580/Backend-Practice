import json
from flask import request
from flask_restful import Resource, abort

from validations import validate_OId
from schedule import Schedule

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

def get_or_abort(s_id):
    res = Schedule.get_by_id(s_id)
    if res is None:
        abort(404, message='No schedule exists with id {}'.format(s_id))
    return res

class ScheduleAPI(Resource):
    def get(self, s_id):
        if not validate_OId(s_id):
            abort(404, message='Invalid id')

        sched = get_or_abort(s_id)
        return vars(sched)

    def put(self, s_id):
        if not validate_OId(s_id):
            abort(404, message='Invalid id')

        data = read_args(request)
        sched = get_or_abort(s_id)

        if 'event_name' not in data:
            abort(404, message='"event_name" field is required to add event to shcedule')

        res = sched.add_event(data['event_name'])
        if res is None:
            abort(404, message='Error adding event to schedule')

        return vars(res), 201

    def delete(self, s_id):
        if not validate_OId(s_id):
            abort(404, message='Invalid id')

        data = read_args(request)
        sched = get_or_abort(s_id)

        if 'event_name' not in data:
            abort(404, message='"event_name" field is required to remove event from shcedule')

        res = sched.remove_event(data['event_name'])
        if res is None:
            abort(404, message='Error removing event from schedule')

        return vars(res)

class SchedulesAPI(Resource):
    def get(self):
        owner = request.args.get('name', default=None)
        return [vars(s) for s in Schedule.get(owner)]

    def post(self):
        data = read_args(request)
        if 'owner' not in data:
            abort(404, message='"owner" field is required to create a schedule')

        sched = Schedule.create(data)
        print(vars(sched))
        return vars(sched), 201
