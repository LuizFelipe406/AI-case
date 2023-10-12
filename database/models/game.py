from ..database import db

class Game(db.Model):
  game_id = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.String(50), nullable=False)
  story = db.Column(db.Text, nullable=False)