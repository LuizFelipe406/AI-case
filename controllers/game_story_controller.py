from flask_restful import Resource
from services.game_story_service import GameStoryService


class GameStoryController(Resource):
    def __init__(self):
        self.service = GameStoryService()

    def get(self, game_id):
        return self.service.get_story(game_id)