import json
from flask import Flask
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

from eventapi import EventAPI, EventsAPI
from scheduleapi import ScheduleAPI, SchedulesAPI

api.add_resource(EventAPI, '/event/<e_id>/')
api.add_resource(EventsAPI, '/event/')

api.add_resource(ScheduleAPI, '/schedule/<s_id>/')
api.add_resource(SchedulesAPI, '/schedule/')

if __name__ == '__main__':
    app.run(debug=True)
