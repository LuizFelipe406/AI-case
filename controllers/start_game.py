import re
import random
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

        if len(player_list) > 4:
            return {"message": "Too many players, limit is 4"}, 400

        context = f"""
          You are an RPG Master who will run a game, this is the start of the game,
          your answer must start with the Game ID following this rules:
            - The answer will start with: Game ID:
            - The ID will be {str(random.randint(10000, 99999))}

          the rpg roles are:
          {rpg_roles}

          you will be given a list of names and must create the rpg characters for each player and return each one of them in a Javascript object, following this rules:
            - name list order needs to be reordered randomly
            - every player must have  a different role, of which must be choosen randomly 
            - this part of the answer will start with the title: "Creating RPG Characters:"
            - you must generate a medieval last name for each character that matches his role, be creative here and increse the temperature of this part
            - you must choose his stats of attack, life, defense and lucky between the values determined in each class
            - each character stats and name must be displayed like a Javascript object
            - all the quotation marks must be single quotes

          next, you will generate the boss they will face, following the rules:
            - This part of the anwser will start with: "The Boss:"
            - the anwser will show each character in a JSON format
          the boss role are:
          {rpg_boss}

          Finally, you will create the scene where the battle will take place, explaining why they are fighting and giving a brief summary of the context, this part will start with: 'The Quest:'""
"""
        response = self.open_ai.generate_answer(context, player_list)
        answer = response.choices[0].message.content
        return self.collect_data(answer, player_list)
    
    def collect_data(self, answer: str, player_list: list):
        answer = answer.replace("\n", "")
        game_id = re.search(r'\d{5}', answer, re.M)
        
        characters = re.findall(r'{[\s\S]*?}', answer, re.M)

        for i in range(len(player_list) + 1):
            character = characters[i]
            #save in db
        
        story_context = re.search(r'(?<=The\sQuest:)[\s\S]*', answer, re.M)

        return {
            "answer": answer,
            "game_id": game_id.group(),
            "characters": characters,
            "story": story_context.group()
        }