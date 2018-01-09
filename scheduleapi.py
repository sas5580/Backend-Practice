from flask_restful import Resource

from app import read_args
from schedule import Schedule

class ScheduleAPI(Resource):
    # Return entire schedule with details info on events
    def get(self, owner):
        sched = Schedule.get(owner)
        return sched.serialize()

    # Add or remove an event to/from a schedule based on args
    def put(self, owner):
        data = read_args(request)
        sched = Schedule.get(owner)
        sched.update(data['event_name'], data['action'])
        return sched.serialize(), 201