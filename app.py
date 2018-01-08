import json
from flask import Flask, request
from flask_restful import Resource, Api, abort

from DataAccessor import DataAccessor
from Model import Event, Schedule

app = Flask(__name__)
api = Api(app)
dao = DataAccessor(app)

def get_event_or_abort(event_name):
    event = dao.get_event(event_name)
    if event is None:
        abort(404, message='Event {} not found'.format(event_name))
    return event

class EventAPI(Resource):
    # Returns event details in JSON format
    def get(self, name):
        event = get_event_or_abort(name)
        return event.serialize()

    # Creates a new event based on args and name
    def post(self, name):
        data = json.loads(request.data)
        data['name'] = name
        event = Event.fromdict(data)
        dao.insert_event(event)
        return name, 201

    # Update exisiting event based on args
    def put(self, name):
        data = json.loads(request.data)
        event = get_event_or_abort(name)
        event.update(
            new_name=data['name'] if 'name' in data else None,
            new_days=data['days'] if 'days' in data else None,
            new_from_time=data['from_time'] if 'from_time' in data else None,
            new_to_time=data['to_time'] if 'to_time' in data else None,
            new_description=data['description'] if 'description' in data else None
        )
        dao.update_event(event)
        return name, 201

    # Deletes the named event
    def delete(self, name):
        dao.remove_event(name)
        return name, 204

class ScheduleAPI(Resource):
    # Return entire schedule with details info on events
    def get(self, owner):
        sched = dao.get_schedule(owner)
        if sched is None:
           abort(404, message='Schedule {} not found'.format(owner))
        return sched.serialize()

    # Add or remove an event to/from a schedule based on args
    def put(self, owner):
        data = json.loads(request.data)
        event = dao.get_event(data['event_name'])
        if event is None:
            abort(404, message='Cannot add/remove {} to/from {}\'s schedule as the event does not exist'.format(data['name'], owner))

        sched = dao.get_schedule(owner)
        if sched is None:
            sched = Schedule(owner, [])
            dao.insert_new_schedule(owner)

        if data['action'] == 'ADD':
            sched.addEvent(event)
        elif data['action'] == 'REMOVE':
            sched.removeEvent(event.name)

        dao.update_schedule(sched)

        return owner, 201
        
api.add_resource(EventAPI, '/event/<name>/')
api.add_resource(ScheduleAPI, '/schedule/<owner>/')

if __name__ == '__main__':
    app.run(debug=True)