import json
from flask import request, jsonify
from flask_restful import Resource, abort

from validations import validate_OId
from schedule import Schedule

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

def create_resp(data, status_code=None):
    resp = jsonify(data)
    if status_code:
        resp.status_code = status_code
    return resp

class ScheduleAPI(Resource):
    def get(self, s_id):
        if not validate_OId(s_id):
            abort(400, message='Invalid id')

        try:
            res = Schedule.get_by_id(s_id)
        except Exception as e:
            abort(500, message='Error retreiving schedule with id {}: {}'.format(s_id, e))

        if res is None:
            abort(404, message='No schedule found with id {}'.format(s_id))

        return create_resp(vars(res))

    def put(self, s_id):
        if not validate_OId(s_id):
            abort(400, message='Invalid id')

        data = read_args(request)
        if 'event_id' not in data or not validate_OId(data['event_id']):
            abort(404, message='"event_id" is missing or invalid')

        try:
            res = Schedule.add_event(s_id, data['event_id'])
        except Exception as e:
            abort(500, message='Error addinge event to schedule: {}'.format(e))

        if res == -1:
            abort(404, message='No event found with id {}'.format(data['event_id']))
        if res == 0:
            abort(404, message='No schedule found with id {}'.format(s_id))

        return create_resp(s_id, 200)

    def delete(self, s_id):
        if not validate_OId(s_id):
            abort(400, message='Invalid id')

        data = read_args(request)
        if 'event_id' not in data or not validate_OId(data['event_id']):
            abort(404, message='"event_id" is missing or invalid')

        try:
            res = Schedule.remove_event(s_id, data['event_id'])
        except Exception as e:
            abort(500, message='Error removing from schedule: {}'.format(e))

        if res < 1:
            abort(404, message='No schedule found with id {}'.format(s_id))

        return create_resp(s_id, 204)

class SchedulesAPI(Resource):
    def get(self):
        owner = request.args.get('owner', default=None)
        return [vars(s) for s in Schedule.get(owner)]

    def post(self):
        data = read_args(request)
        if 'owner' not in data:
            abort(404, message='"owner" field is required to create a schedule')
        try:
            sched = Schedule.create(data)
        except Exception as e:
            abort(500, message='Error creating schedule: {}'.format(e))

        return create_resp(vars(sched), 201)
