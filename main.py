from flask import Flask
from flask_restful import Api
from controllers.question import Question
from controllers.solve import Solve

app = Flask(__name__)
api = Api(app)

api.add_resource(Question, "/question/<string:subject>")
api.add_resource(Solve, "/solve/<string:subject>")


if __name__ == '__main__':
    app.run(debug=True)