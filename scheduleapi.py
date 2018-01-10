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
            abort(400, message='Invalid id')

        sched = get_or_abort(s_id)
        return vars(sched)

    def put(self, s_id):
        if not validate_OId(s_id):
            abort(400, message='Invalid id')

        data = read_args(request)
        sched = get_or_abort(s_id)

        if 'event_id' not in data or not validateOId(data['event_id']):
            abort(404, message='"event_id" is missing or invalid')

        try:
            res = sched.add_event(data['event_id'])
        except Exception as e:
            abort(500, message='Error addinge event to schedule: {}'.format(e))

        return vars(res), 201

    def delete(self, s_id):
        if not validate_OId(s_id):
            abort(400, message='Invalid id')

        data = read_args(request)
        sched = get_or_abort(s_id)

        if 'event_id' not in data or not validateOId(data['event_id']):
            abort(404, message='"event_id" is missing or invalid')

        try:
            res = sched.remove_event(data['event_id'])
        except Exception as e:
            abort(500, message='Error removing from schedule: {}'.format(e))

        return vars(res)

class SchedulesAPI(Resource):
    def get(self):
        owner = request.args.get('name', default=None)
        return [vars(s) for s in Schedule.get(owner)]

    def post(self):
        data = read_args(request)
        if 'owner' not in data:
            abort(404, message='"owner" field is required to create a schedule')
        try:
            sched = Schedule.create(data)
        except Exception as e:
            abort(500, message='Error creating schedule: {}'.format(e))

        return vars(sched), 201
