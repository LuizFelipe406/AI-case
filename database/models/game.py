from ..database import db

class Game(db.Model):
  GameId = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.String, nullable=False)
  story = db.Column(db.String, nullable=False)