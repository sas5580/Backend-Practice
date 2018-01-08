import json
from flask import Flask, request

from flask_restful import Resource, Api, abort

from DataAccessor import DataAccessor
from Model import Time, Event, Schedule

app = Flask(__name__)
api = Api(app)

# TODO: the DAO should not be accessed by the APP 
# TODO: the APP should communicate with the MODEL which handles all business logic
dao = DataAccessor(app)

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

# TODO: this method is what should be implemented within the MODEL, this handles all the logic around
# retrieving an entity
def get_event_or_abort(event_name):
    # TODO: similar to above, remove all DAO requests to the model, APP <-> MODEL <-> DAO
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
        data = read_args(request)
        data['name'] = name
        event = Event.fromdict(data)
        
        # TODO: similar to above, remove all DAO requests to the model, APP <-> MODEL <-> DAO
        dao.insert_event(event)
        
        return name, 201

    # Update exisiting event based on args
    def put(self, name):
        data = read_args(request)
        event = get_event_or_abort(name)
        event.update(
            new_name=data['name'] if 'name' in data else None,
            new_days=data['days'] if 'days' in data else None,
            new_from_time=Time.fromdict(data['from_time']) if 'from_time' in data else None,
            new_to_time=Time.fromdict(data['to_time']) if 'to_time' in data else None,
            new_description=data['description'] if 'description' in data else None
        )
        
        # TODO: similar to above, remove all DAO requests to the model, APP <-> MODEL <-> DAO
        dao.update_event(event)
        
        return name, 201

    # Deletes the named event
    def delete(self, name):
        # TODO: similar to above, remove all DAO requests to the model, APP <-> MODEL <-> DAO
        dao.remove_event(name)
        
        return name, 204

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