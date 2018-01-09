from app import api, app
from eventapi import EventAPI
from scheduleapi import ScheduleAPI

api.add_resource(EventAPI, '/event/<name>/')
api.add_resource(ScheduleAPI, '/schedule/<owner>/')
