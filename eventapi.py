import json
from flask import request
from flask_restful import Resource

from event import Event

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

class EventAPI(Resource):
    # Returns event details in JSON format
    def get(self, name):
        event = Event.get(name)
        return event.serialize()

    # Creates a new event based on args and name
    def post(self, name):
        event_dict = read_args(request)
        event = Event.create(name, event_dict)
        return event.serialize(), 201

    # Update exisiting event based on args
    def put(self, name):
        update_dict = read_args(request)
        event = Event.get(name)
        event.update(update_dict)
        return event.serialize(), 201

    # Deletes the named event
    def delete(self, name):
        Event.delete(name)
        return name, 204