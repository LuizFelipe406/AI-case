from flask_restful import Resource
from flask import request
from open_ai.open_ai import OpenAI
from rpg_basic_rules import rpg_roles, rpg_boss

class StartGame(Resource):
    def __init__(self):
        self.open_ai = OpenAI()

    def get(self):
        data = request.get_json(force=True)
        player_list = data.get('playerList', [])

        # if len(player_list) > 4:
        #     return {"message": "Too many players, limit is 4"}, 400

        context = f"""
          You are an RPG Master who will run a game, this is the start of the game,
          your answer must start with the game id, a unique number with 5 characters.

          the rpg roles are:
          {rpg_roles}

          u will be given a list of 4 names and you must create the rpg characters for each player following the roles and this following rules:
            - every player must have  a different role, witch will be chosen randomly, not mattering the order the names apper on the list
            - you must generate a last name for each character that matches his role, but his last name cannot be the name of the role
            - you must choose his stats of attack, life, defense and lucky between the values ​​determined in each class

          next, you will generate the boss they will face
          the boss role are:
          {rpg_boss}

          finally, generate the scene where the battle will take place, explaining why they are fighting and giving a brief summary of the context
"""
        return self.open_ai.generate_answer(context, player_list)