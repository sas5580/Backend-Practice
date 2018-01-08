import json
from flask import Flask, request
from flask_restful import Resource, Api, abort

from DataAccessor import DataAccessor
from Model import Event, Schedule

app = Flask(__name__)
api = Api(app)
dao = DataAccessor(app)

def get_event_or_abort(event_name):
    event = dao.getEvent(event_name)
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
        dao.insertEvent(event)
        return name, 201

    # Update exisiting event based on args
    def put(self, name):
        data = json.loads(request.data)
        event = get_event_or_abort(name)
        event.update(
            newName=data['name'] if 'name' in data else None,
            newDays=data['days'] if 'days' in data else None,
            newFromTime=data['fromTime'] if 'fromTime' in data else None,
            newToTime=data['toTime'] if 'toTime' in data else None,
            newDescription=data['description'] if 'description' in data else None
        )
        dao.update_event(event)
        return name, 201

    # Deletes the named event
    def delete(self, name):
        dao.removeEvent(name)
        return name, 204

class ScheduleAPI(Resource):
    # Return entire schedule with details info on events
    def get(self, owner):
        sched = dao.getSchedule(owner)
        if sched is None:
           abort(404, message='Schedule {} not found'.format(owner))
        return sched.serialize()

    # Add or remove an event to/from a schedule based on args
    def put(self, owner):
        data = json.loads(request.data)
        event = dao.getEvent(data['event_name'])
        if event is None:
            abort(404, message='Cannot add/remove {} to/from {}\'s schedule as the event does not exist'.format(data['name'], owner))

        sched = dao.getSchedule(owner)
        if sched is None:
            sched = Schedule(owner, [])
            dao.insertNewSchedule(owner)

        if data['action'] == 'ADD':
            sched.addEvent(event)
        elif data['action'] == 'REMOVE':
            sched.removeEvent(event.name)

        dao.updateSchedule(sched)

        return owner, 201

api.add_resource(EventAPI, '/event/<name>/')
api.add_resource(ScheduleAPI, '/schedule/<owner>/')

if __name__ == '__main__':
    app.run(debug=True)