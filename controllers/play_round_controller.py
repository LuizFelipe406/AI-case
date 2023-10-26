import re
import random
import json
from flask_restful import Resource
from flask import request
from open_ai.open_ai import OpenAI
from database.database import db
from database.models import Character, Game
from services.play_round_service import PlayRoundService

#  to be done:
#   get lucky to be re-cauculated every round for each character
#   give chat gpt how much damage each player shoud caus at the round insted of giving a formula


class PlayRoundController(Resource):
    def __init__(self):
        self.service = PlayRoundService()

    def get(self, game_id):
        data = request.get_json(force=True)
        user_input: str = data.get('input')

        return self.service.play(game_id, user_input)