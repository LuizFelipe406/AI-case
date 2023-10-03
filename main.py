from flask import Flask
from flask_restful import Api
from controllers.start_game import StartGame

app = Flask(__name__)
api = Api(app)

api.add_resource(StartGame, "/game/start")

if __name__ == '__main__':
    app.run(debug=True)