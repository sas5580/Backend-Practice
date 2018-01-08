import json
from flask import Flask, request

from flask_restful import Resource, Api, abort

from DataAccessor import DataAccessor
from Model import Time, Event, Schedule

app = Flask(__name__)
api = Api(app)

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

# TODO: these are two different API resources, they should exist within their own app files along with individual model,
# and dao objects
class ScheduleAPI(Resource):
    # Return entire schedule with details info on events
    def get(self, owner):
        
        # TODO: similar to above, remove all DAO requests to the model, APP <-> MODEL <-> DAO
        sched = dao.get_schedule(owner)
        
        if sched is None:
           abort(404, message='Schedule {} not found'.format(owner))
        return sched.serialize()

    # Add or remove an event to/from a schedule based on args
    def put(self, owner):
        data = read_args(request)
        
        # TODO: similar to above, remove all DAO requests to the model, APP <-> MODEL <-> DAO
        event = dao.get_event(data['event_name'])
        
        if event is None:
            abort(404, message='Cannot add/remove {} to/from {}\'s schedule as the event does not exist'.format(data['name'], owner))
        
        # TODO: similar to above, remove all DAO requests to the model, APP <-> MODEL <-> DAO
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