from flask_pymongo import PyMongo

from Model import Event, Schedule

DB_NAME = 'schedule_practice'
DB_USERNAME = 'admin'
DB_PASSWORD = 'admin'
DB_URI = 'mongodb://%s:%s@ds239387.mlab.com:39387/schedule_practice' % (DB_USERNAME, DB_PASSWORD)





# TODO: these DAO classes should be implemented for each resource and model required
# the DAO is to handle the unique query constraints for each service and is meant to only ever
# modify the resource it is built for.

# TODO: the methods implemented in here should be that of save(), get_by_id(), get_by_params(), delete(), update()
# TODO: the methods explained above will handle all the query logic for whatever the DataSource is that we use, this way
# we can just swap out Mongo for Postgres for example at any time and only ever have to modify one file.

# TODO: please refactor the logic within here to handle this, be sure to have singular DAO classes for Event and Schedule

class DataAccessor:

    def __init__(self, app):
        app.config['MONGO_DBNAME'] = DB_NAME
        app.config['MONGO_URI'] = DB_URI
        self.__mongo = PyMongo(app)

        print('Connected to DB!')

    """
    Read Operations
    """
    def __find(self, collection, selector):
        return self.__mongo.db[collection].find_one(selector)

    def get_event(self, event_name: str) -> Event:
        res = self.__find('event', {'name': event_name})
        if res is None:
            return None
        return Event.fromdict(res)

    def get_schedule(self, schedule_owner: str) -> Schedule:
        res = self.__find('schedule', {'owner': schedule_owner})
        if res is None:
            return None
        return Schedule(schedule_owner, [self.get_event(e_name) for e_name in res['events']])

    """
    Write Operations
    """

    def __insert(self, collection, document):
        if isinstance(document, dict):
            self.__mongo.db[collection].insert_one(document)
        elif isinstance(document, list) or isinstance(document, tuple):
            self.__mongo.db[collection].insert_many(document)

    def __update(self, collection, selector, updated_document):
        self.__mongo.db[collection].update_many(selector, {'$set': updated_document})

    def __remove(self, collection, selector):
        self.__mongo.db[collection].delete_many(selector)

    def insert_event(self, event: Event):
        self.__insert('event', event.serialize())

    def update_event(self, event: Event):
        self.__update('event', {'name': event.name}, event.serialize())

    def remove_event(self, eventName: str):
        self.__remove('event', {'name': eventName})

    def insert_new_schedule(self, owner: str):
        self.__insert('schedule', {'owner': owner, 'events': []})

    def update_schedule(self, new_sched: Schedule):
        self.__update('schedule', {'owner': new_sched.owner}, {'events': [e.name for e in new_sched.events]})

    def remove_schedule(self, owner: str):
        self.__remove('schedule', {'owner': owner})






