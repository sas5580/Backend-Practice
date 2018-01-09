import json
from flask import Flask
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

from eventapi import EventAPI
from scheduleapi import ScheduleAPI

api.add_resource(EventAPI, '/event/<name>/')
api.add_resource(ScheduleAPI, '/schedule/<owner>/')
