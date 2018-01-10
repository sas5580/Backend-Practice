import json
from datetime import datetime
from flask import request
from flask_restful import Resource, abort

from event import Event
from eventvalidations import validate_put, validate_post
from validations import validate_OId

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

class EventAPI(Resource):
    def get(self, e_id):
        if not validate_OId(e_id):
            abort(400, message='Invalid id')
        event = Event.get_by_id(e_id)
        if event is None:
            abort(404, message='Event with id "{}" not found'.format(id_str))
        return vars(event)

    def put(self, e_id):
        data = read_args(request)
        try:
            validate_put(e_id, data)
        except Exception as e:
            abort(400, message='Invalid payload to update event: {}'.format(e))

        event = Event.get_by_id(e_id)
        if event is None:
            abort(404, message='Event with id "{}" not found'.format(id_str))

        event.update(data)
        return vars(event), 201

    def delete(self, e_id):
        if not validate_OId(e_id):
            abort(400, message='Invalid id')
        if not Event.delete(e_id):
            abort(404, messsage='Error deleting event with id {}'.format(e_id))
        return e_id, 204

class EventsAPI(Resource):
    def post(self):
        data = read_args(request)
        try:
            validate_post(data)
        except Exception as e:
            abort(400, message='Invalid payload to create event: {}'.format(e))

        event = Event.create(data)
        return vars(event), 201

    def get(self):
        name = request.args.get('name', default=None)
        return [vars(e) for e in Event.get(name)]
