import os
from pymongo import MongoClient
from bson.objectid import ObjectId

DB_NAME = 'schedule_practice'

class DAO:
    __db = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)[DB_NAME]

    """
    Read Operations
    """
    def _get_by_id(self, collection, id_str):
        return self.__db[collection].find_one({'_id': ObjectId(id_str)})

    def _get_by_params(self, collection, selector):
        return list(self.__db[collection].find(selector))

    """
    Write Operations
    """

    def _save_one(self, collection, document):
        res = self.__db[collection].insert_one(document)
        if res.acknowledged:
            return str(res.inserted_id)
        return None

    def _save_many(self, collection, documents_list):
        res = self.__db[collection].insert_many(documents_list)
        if res.acknowledged:
            return [str(_id) for _id in res.inserted_ids]
        return None

    def _update(self, collection, selector, updated_document, upsert=False):
        res = self.__db[collection].update_many(selector, {'$set': updated_document}, upsert=upsert)
        return res.acknowledged

    def _delete(self, collection, selector):
        res = self.__db[collection].delete_many(selector)
        return res.acknowledged
