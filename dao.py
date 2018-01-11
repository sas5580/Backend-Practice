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
        return str(res.inserted_id) if res.acknowledged else None

    def _count(self, collection, filter_doc):
        return self.__db[collection].count(filter_doc)

    def _update(self, collection, selector, updated_document):
        res = self.__db[collection].update_many(selector, {'$set': updated_document}, upsert=upsert)
        return res.matched_count if res.acknowledged else 0

    def _addToSet(self, collection, selector, push_document):
        res = self.__db[collection].update_many(selector, {'$addToSet': push_document})
        return res.matched_count if res.acknowledged else 0

    def _pull(self, collection, selector, pull_document):
        res = self.__db[collection].update_many(selector, {'$pull': pull_document})
        return res.matched_count if res.acknowledged else 0

    def _delete(self, collection, selector):
        res = self.__db[collection].delete_many(selector)
        return res.acknowledged
