import re
import random
import json
from flask_restful import Resource
from flask import request
from open_ai.open_ai import OpenAI
from rpg_basic_rules import rpg_roles, rpg_boss
from sqlalchemy import delete
from database.database import db
from database.models import Character, Game

class PlayRound(Resource):
    def __init__(self):
        self.open_ai = OpenAI()

    def get(self, game_id):
        data = request.get_json(force=True)
        user_input: str = data.get('input')

        game: Game = db.get_or_404(Game, game_id)
        characters: list[Character] = Character.query.filter(Character.game_id == game.game_id).all()

        context = f"""
          You are an RPG Master who will run a game, this is the first round of the game,
          your answer must start with the Game ID following this rules:
            - The answer will start with: Game ID:
            - The ID will be {game.game_id}

          The characters for context only:
          {characters}

          the story of the game for context only:
          {game.story}

          You need to develop the story of the first round of the RPG, this part will start with the title "The Story:", where players will encounter the boss for the first time and carry out an attack,
          every player will atack the boss once (except the healer who will only heal the characters and cant attack the boss) and the boss will atack only half of the total players numbers.

          The rules of an attack are:
          - you need to calculate the attack damage delt and the life remaining of the defender after each character attack
          - the attack is calculated by this formula: life = (attack points of the attacker + lucky points of the attacker) - ((defense points of the defender + lucky points of the defender) / 2).
          - the healer can only heal one player per round and the amount of heal given is heal + lucky.
          - the healer will only move after the boss attack is completed
          - if a player gets a life less than zero, the life will stay at zero and should not be negative.
          - a healer cannot revive a player, once his life gets to zero, he cannot heal that character anymore.

          After the attack, you need to develop the story giving the user 2 different possibilities that the story can have on the next round of the game, be creative and let the story develop in two different ways, this resume should have about 3 lines each, this part will start with the title "On Next Round:"

          After the possibilities, you will return all current attributes of every character like a Javascript object each, this part will start with the title The Characters:       
"""
        response = self.open_ai.generate_answer(context, user_input)
        answer = response.choices[0].message.content
        try:
          return self.collect_data(answer, game)
        except Exception as e:
            return { "error": "chat gpt did not respond in correct formart, try again please"}, 500
    
    def collect_data(self, answer: str, game: Game):
        answer = answer.replace("\n", "")
        game.status = 'on going'
        game.story = re.search(r'(?<=The\sStory:)[\s\S]*(?=On\sNext\sRound:)', answer, re.M).group()
        
        try:
          characters: list[str] = re.findall(r'{[\s\S]*?}', answer, re.M)
          for c in characters:
              character_dict = json.loads(c)
              print(character_dict)
              character_in_db = db.session.get(Character, character_dict["id"])
              print(character_in_db)
              character_in_db.role = character_dict["role"]
              character_in_db.type = character_dict["type"]
              character_in_db.name = character_dict["name"]
              character_in_db.life = character_dict["life"]
              character_in_db.defense = character_dict["defense"]
              character_in_db.lucky = character_dict["lucky"]
              character_in_db.attack = character_dict.get("attack", None)
              character_in_db.heal = character_dict.get("heal", None)
        except Exception as e:
            raise Exception

        db.session.commit()
        return {
            "game_id": game.game_id,
            "characters": characters,
            "story": game.story,
            "on_the_next_round": re.search(r'(?<=On\sNext\sRound:)[\s\S]*(?=The\sCharacters:)', answer, re.M).group(),
            "answer": answer
        }