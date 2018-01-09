import json
from flask import Flask, request
from flask_restful import Resource, Api, abort

from eventapi import EventAPI
from scheduleapi import ScheduleAPI

def read_args(request):
    return json.loads(request.data.decode('utf-8'))

app = Flask(__name__)
api = Api(app)
        
api.add_resource(EventAPI, '/event/<name>/')
api.add_resource(ScheduleAPI, '/schedule/<owner>/')