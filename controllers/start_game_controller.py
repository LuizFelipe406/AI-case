from flask_restful import Resource
from flask import request
from services.start_game_service import StartGameService

class StartGameController(Resource):
    def __init__(self):
        self.service = StartGameService()

    def post(self):
        data = request.get_json(force=True)
        player_list = data.get('playerList', [])

        if len(player_list) > 4:
            return {"message": "Too many players, limit is 4"}, 400

        return self.service.start(player_list)