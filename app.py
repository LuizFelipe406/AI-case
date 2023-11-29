import os
from flask import Flask
from flask_restful import Api
from database.database import db
from database import Character, Game
from controllers import StartGameController, PlayRoundController, GameStoryController

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}/rpgdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

api.add_resource(StartGameController, "/game/start")
api.add_resource(PlayRoundController, "/game/play/<int:game_id>")
api.add_resource(GameStoryController, "/game/story/<int:game_id>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)