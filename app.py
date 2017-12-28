from flask import Flask
from flask_restful import Resource, Api
from DataAccessor import DataAccessor

app = Flask(__name__)
api = Api(app)
dao = DataAccessor(app)

class HelloWorld(Resource):
    def get(self, op):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/<op>')

if __name__ == '__main__':
    app.run(debug=True)