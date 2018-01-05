import json
from flask import Flask, request
from flask_restful import Resource, Api, abort

from DataAccessor import DataAccessor
from Model import Event, Schedule

app = Flask(__name__)
api = Api(app)
dao = DataAccessor(app)

class EventAPI(Resource):
    # Returns event details in JSON format
    def get(self, name):
        event = dao.getEvent(name)
        if event is None:
            abort(404, message='Event {} not found'.format(name))
        return event.serialize()

    # Creates a new event based on args and name
    def post(self, name):
        data = json.loads(request.data)
        data['name'] = name
        event = Event.fromdict(data)
        dao.insertEvent(event)
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
            print(sched.serialize())
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