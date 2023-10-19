from flask import Flask
from flask_restful import Api
from database.database import db
from database import Character, Game
from controllers import StartGame, PlayRound

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/rpgdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

api.add_resource(StartGame, "/game/start")
api.add_resource(PlayRound, "/game/play/<int:game_id>")

if __name__ == '__main__':
    app.run(debug=True)