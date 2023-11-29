from database.database import db
from database.models import Game, Character


class GameStoryService():
  def get_story(self, game_id):
    game: Game = db.get_or_404(Game, game_id)

    characters: list[Character] = Character.query.filter(Character.game_id == game.game_id).all()
    characters_list = [character.as_dict() for character in characters]

    return {
      "game_id": game.game_id,
      "status": game.status,
      "story": game.story,
      "characters": characters_list
    }