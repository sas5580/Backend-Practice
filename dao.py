from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from app import app

DB_NAME = 'schedule_practice'
DB_USERNAME = 'admin'
DB_PASSWORD = 'admin'
DB_URI = 'mongodb://%s:%s@ds239387.mlab.com:39387/schedule_practice' % (DB_USERNAME, DB_PASSWORD)

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
        res = None
        if isinstance(document, dict):
            res = self.__mongo.db[collection].insert_one(document)
        elif isinstance(document, list) or isinstance(document, tuple):
            res = self.__mongo.db[collection].insert_many(document)
        return res.acknowledged if res is not None else False

    def _update(self, collection, selector, updated_document):
        res = self.__mongo.db[collection].update_many(selector, {'$set': updated_document})
        return res.acknowledged

    def _delete(self, collection, selector):
        res = self.__mongo.db[collection].delete_many(selector)
        return res.acknowledged






