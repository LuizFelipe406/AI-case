from ..database import db
from database.models.game import Game

class Character(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  game_id = db.Column(db.Integer, db.ForeignKey(Game.game_id), nullable=False)
  role = db.Column(db.String(50), nullable=False)
  type = db.Column(db.String(50), nullable=False)
  name = db.Column(db.String(50), nullable=False)
  life = db.Column(db.Integer, nullable=False)
  defense = db.Column(db.Integer, nullable=False)
  lucky = db.Column(db.Integer, nullable=False)
  attack = db.Column(db.Integer)
  heal = db.Column(db.Integer)

  def __repr__(self):
        return (
            f"{{'id': {self.id}, 'game_id': {self.game_id}, 'role': '{self.role}', "
            f"'type': '{self.type}', 'name': '{self.name}', 'life': {self.life}, "
            f"'defense': {self.defense}, 'lucky': {self.lucky}, 'attack': {self.attack}, "
            f"'heal': {self.heal}}}"
        )
  
  def as_dict(self):
    return {
        "id": self.id,
        "game_id": self.game_id,
        "role": self.role,
        "type": self.type,
        "name": self.name,
        "life": self.life,
        "defense": self.defense,
        "lucky": self.lucky,
        "attack": self.attack,
        "heal": self.heal,
    }