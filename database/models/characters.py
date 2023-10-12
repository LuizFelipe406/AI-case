from ..database import db
from database.models.game import Game

class Characters(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  GameId = db.Column(db.Integer, db.ForeignKey(Game.GameId), nullable=False)
  role = db.Column(db.String, nullable=False)
  type = db.Column(db.String, nullable=False)
  name = db.Column(db.String, nullable=False)
  life = db.Column(db.Integer, nullable=False)
  defense = db.Column(db.Integer, nullable=False)
  lucky = db.Column(db.Integer, nullable=False)
  attack = db.Column(db.Integer)
  heal = db.Column(db.Integer)