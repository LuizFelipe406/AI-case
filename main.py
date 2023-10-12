from flask import Flask
from flask_restful import Api
from database.database import db
from database.models import Character, Game
from controllers.start_game import StartGame

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@db/airpg'
db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

api.add_resource(StartGame, "/game/start")

if __name__ == '__main__':
    app.run(debug=True)