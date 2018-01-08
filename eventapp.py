from flask_restful import Resource

from app import read_args
from event import Event

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
        event = Event.delete(name)
        return event.serialize(), 204