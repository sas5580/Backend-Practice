from flask_pymongo import PyMongo
from bson.objectid import ObjectId

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

class DAO:
    app.config['MONGO_DBNAME'] = DB_NAME
    app.config['MONGO_URI'] = DB_URI
    __mongo = PyMongo(app)

    """
    Read Operations
    """
    def _get_by_id(self, collection, id_str:str):
        return self.__mongo.db[collection].find_one({'_id': ObjectId(id_str)})

    def _get_by_params(self, collection, selector):
        return self.__mongo.db[collection].find_one(selector)

    """
    Write Operations
    """

    def _save(self, collection, document):
        if isinstance(document, dict):
            self.__mongo.db[collection].insert_one(document)
        elif isinstance(document, list) or isinstance(document, tuple):
            self.__mongo.db[collection].insert_many(document)

    def _update(self, collection, selector, updated_document):
        self.__mongo.db[collection].update_many(selector, {'$set': updated_document})

    def _delete(self, collection, selector):
        self.__mongo.db[collection].delete_many(selector)






