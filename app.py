import json
from flask import Flask, request
from flask_restful import Resource, Api, abort

from DataAccessor import DataAccessor
from Model import Event, Schedule

app = Flask(__name__)
api = Api(app)
dao = DataAccessor(app)

class EventAPI(Resource):
    def get(self, name):
        event = dao.getEvent(name)
        if event is None:
            abort(404, message='Event {} not found'.format(name))
        return event.serialize()

    def post(self, name):
        data = json.loads(request.data)
        data['name'] = name
        event = Event.fromdict(data)
        dao.insertEvent(event)
        return name, 201

    def delete(self, name):
        dao.removeEvent(name)
        return name, 204

class ScheduleAPI(Resource):
    def get(self, owner):
        return #dao.find('schedule', {'owner': owner})

api.add_resource(EventAPI, '/event/<name>/')
api.add_resource(ScheduleAPI, '/schedule/<owner>/')

if __name__ == '__main__':
    app.run(debug=True)