from flask_restful import Resource
from flask import request
from services.play_round_service import PlayRoundService


class PlayRoundController(Resource):
    def __init__(self):
        self.service = PlayRoundService()

    def get(self, game_id):
        data = request.get_json(force=True)
        user_input: str = data.get('input')

        return self.service.play(game_id, user_input)