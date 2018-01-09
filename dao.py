from pymongo import MongoClient
from bson.objectid import ObjectId

DB_NAME = 'schedule_practice'
DB_USERNAME = 'admin'
DB_PASSWORD = 'admin'
DB_URI = 'mongodb://%s:%s@ds239387.mlab.com:39387/schedule_practice' % (DB_USERNAME, DB_PASSWORD)

class DAO:
    __db = MongoClient(DB_URI)[DB_NAME]

    """
    Read Operations
    """
    def _get_by_id(self, collection, id_str):
        return self.__db[collection].find_one({'_id': ObjectId(id_str)})

    def _get_many_by_params(self, collection, selector):
        return self.__db[collection].find(selector)

    def _get_one_by_params(self, collection, selector):
        return self.__db[collection].find_one(selector)

    """
    Write Operations
    """

    def _save_one(self, collection, document):
        res = self.__db[collection].insert_one(document)
        return res.acknowledged

    def _save_many(self, collection, documents_list):
        res = self.__db[collection].insert_many(documents_list)
        return res.acknowledged

    def _update(self, collection, selector, updated_document, upsert=False):
        res = self.__db[collection].update_many(selector, {'$set': updated_document}, upsert=upsert)
        return res.acknowledged

    def _delete(self, collection, selector):
        res = self.__db[collection].delete_many(selector)
        return res.acknowledged
