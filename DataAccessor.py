from flask_pymongo import PyMongo

DB_NAME = 'schedule_practice'
DB_USERNAME = 'admin'
DB_PASSWORD = 'admin'
DB_URI = 'mongodb://%s:%s@ds239387.mlab.com:39387/schedule_practice' % (DB_USERNAME, DB_PASSWORD)

class DataAccessor(object):

    def __init__(self, app):
        app.config['MONGO_DBNAME'] = DB_NAME
        app.config['MONGO_URI'] = DB_URI
        self.mongo = PyMongo(app)

        print('Connected to DB!')

    # Insert a document (dict) into specified collection
    def insert(self, collection, document):
        if isinstance(document, dict):
            self.mongo.db[collection].insert_one(document)
        elif isinstance(document, list) or isinstance(document, tuple):
            self.mongo.db[collection].insert_many(document)

    # Returns all documents that satisfy specified selector (dict)
    def get(self, collection, selector):
        res = self.mongo.db[collection].find_one(selector)
        return res

    # Updates documents that satisfied the selector with the given updated document
    def update(self, collection, selector, updated_document):
        print("UPDATE")
        self.mongo.db[collection].update_many(selector, {'$set': updated_document})

    # Removes documents that match the given selector
    def remove(self, collection, selector):
        print("REM")
        self.mongo.db[collection].delete_many(selector)




