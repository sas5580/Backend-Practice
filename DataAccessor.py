from flask_pymongo import PyMongo

from Model import Time, Event, Schedule

DB_NAME = 'schedule_practice'
DB_USERNAME = 'admin'
DB_PASSWORD = 'admin'
DB_URI = 'mongodb://%s:%s@ds239387.mlab.com:39387/schedule_practice' % (DB_USERNAME, DB_PASSWORD)

class DataAccessor:

    def __init__(self, app):
        app.config['MONGO_DBNAME'] = DB_NAME
        app.config['MONGO_URI'] = DB_URI
        self.__mongo = PyMongo(app)

        print('Connected to DB!')

    """
    Read Operations
    """
    def getSchedule(self, scheduleOwner):
        res = self.__mongo.db.schedule.find_one({'owner': scheduleOwner})
        if res is None:
            return None
        return Schedule.fromdict(res)

    """
    Write Operations
    """

    # Insert a document (dict) into specified collection
    def insert(self, collection, document):
        if isinstance(document, dict):
            self.__mongo.db[collection].insert_one(document)
        elif isinstance(document, list) or isinstance(document, tuple):
            self.__mongo.db[collection].insert_many(document)

    # Updates documents that satisfied the selector with the given updated document
    def update(self, collection, selector, updated_document):
        print("UPDATE")
        self.__mongo.db[collection].update_many(selector, {'$set': updated_document})

    # Removes documents that match the given selector
    def remove(self, collection, selector):
        print("REM")
        self.__mongo.db[collection].delete_many(selector)






