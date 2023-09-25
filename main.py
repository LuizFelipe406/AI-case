from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self, name):
        return {
            "message": "hello world, " + name
        }

api.add_resource(HelloWorld, "/hi/<string:name>")

if __name__ == '__main__':
    app.run(debug=True)