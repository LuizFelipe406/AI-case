import re
import random
import json
import math
from flask_restful import Resource
from open_ai.open_ai import OpenAI
from database.database import db
from database.models import Character, Game
from rpg_basic_rules import lucky_by_role

class PlayRoundService(Resource):
    def __init__(self):
        self.open_ai = OpenAI()

    def play(self, game_id:str, user_input:str):
        game: Game = db.get_or_404(Game, game_id)
        if game.status == 'finished':
            return {'message': 'game already finished'}, 400

        characters: list[Character] = Character.query.filter(Character.game_id == game.game_id).all()
        characters_list = []
        for character in characters:
            character.lucky = self.calculate_lucky(character)
            characters_list.append(character.as_dict())

        initial_context = 'You are an RPG Master who will run a game, this is the first round of the game' if game.status == 'started' else 'You are an RPG Master who will be continuing a round of the game'

        context_instructions = 'You need to develop the story of the first round of the RPG, this part will start with the title "The Story:", where players will encounter the boss for the first time and carry out an attack, every player will atack the boss once (except the healer who will only heal the characters after the boss attack and cant attack the boss) and the boss will atack only half of the total players numbers.' if game.status == 'started' else 'You are going to receive the user input about how he would like the story to continue, with that, you will create the story of this round based on the input and being creative, this part will start with the title "The Story:", be aware that this round must include an attack beetwen the players and the boss, every player must strike the boss once, and the boss can only attack half of the current alive players (except the healer who will only heal the characters after the boss attack and cant attack the boss)'

        attack_instructions = self.calculate_attack(characters)

        context = f"""
          {initial_context}
          Your answer will have 4 topics:
            - Game ID
            - The Story
            - On Next Round/The End
            - The Characters

          The characters for context only, you should not return this at the beginning:
          {characters_list}

          the story of the game for context only, you should not return this at the beginning:
          {game.story}
            
          Game ID:
          
          your answer must start with the Game ID following this rules:
            - The answer will start with: Game ID:
            - The ID will be {game.game_id}

          The Story:

          {context_instructions}

          Follow the instructions bellow to guide the attacks:
          {attack_instructions}
          - you need to calculate the life remaining of the defender after each character attack
          - the healer can only heal one character per round.
          - the healer will only move after the boss attack is completed
          - if a character gets a life less than zero, the life will stay at zero and should not be negative.
          - a healer cannot revive a character, once his life gets to zero, he cannot heal that character anymore.
          
          On Next Round/The End:

          If all of the players and the boss are still alive, life != 0 after the attack, you need to develop the story giving the user 2 different possibilities that the story can have on the next round of the game, be creative and let the story develop in two different ways, this resume should have about 3 lines each, this part will start with the title "On Next Round:"

          If all of the players or the boss are dead, life == 0 after the attack, you need to finalize the story, giving the RPG a nice and creative ending, this part will start with the title "The End:", be aware, this part should only be included if all of the players died or the boss is defeated, life == 0.

          The Characters:

          At the end, you will return all current attributes of every character like a Javascript object each, starting with one silge curly brackets for each, this part will start with the title The Characters:
          example:
           Warrior: {{
              id: xxxx,
	            role: xxxx,
              type: xxxx,
	            name: xxxx,
              attack: xxxx,
	            life: xxxx,
	            defense: xxxx,
	            lucky: xxxx
            }}  
"""
        response = self.open_ai.generate_answer(context, user_input)
        answer = response.choices[0].message.content
        try:
          return self.collect_data(answer, game)
        except Exception as e:
            return { "error": "chat gpt did not respond in correct formart, try again please" }, 500
    
    def collect_data(self, answer: str, game: Game):
        answer = answer.replace("\n", "")
        answer_ending = re.match(r'(?<=The\sEnd:)[\s\S]*(?=The\sCharacters:)', answer, re.M)
        answer_round_story = re.search(r'(?<=The\sStory:)[\s\S]*(?=On\sNext\sRound:)', answer, re.M).group()

        game.status = 'on going' if answer_ending is None else 'finished'
        game.story = game.story + answer_round_story
        
        if game.status == 'finished':
            game.story = game.story + answer_ending.group()

        try:
          characters: list[str] = re.findall(r'{[\s\S]*?}', answer, re.M)
          for c in characters:
              character_dict = json.loads(c)
              character_in_db = db.session.get(Character, character_dict["id"])
              character_in_db.role = character_dict["role"]
              character_in_db.type = character_dict["type"]
              character_in_db.name = character_dict["name"]
              character_in_db.life = character_dict["life"]
              character_in_db.lucky = character_dict["lucky"]
        except Exception as e:
            raise Exception

        db.session.commit()
        return {
            "game_id": game.game_id,
            "characters": characters,
            "full_story": game.story,
            "round_story": answer_round_story,
            "on_the_next_round": re.search(r'(?<=On\sNext\sRound:)[\s\S]*(?=The\sCharacters:)', answer, re.M).group() if game.status != 'finished' else 'Game Over.'
        }
    
    def calculate_lucky(self, character: Character):
        character_lucky_min = lucky_by_role[character.role][0]
        character_lucky_max = lucky_by_role[character.role][1]
        return random.randint(character_lucky_min, character_lucky_max)
       

    def calculate_attack(self, characters: list[Character]):
        result = ""
        for character in characters:
          if character.role != "Healer" and character.life > 0:
              result = result + f"- the character {character.name} will deal {character.attack  + character.lucky} damage and take {math.floor((character.defense + character.lucky) / 2)} less damage this round\n"
          if character.role == "Healer" and character.life > 0:
              result = result + f"- the character {character.name} will heal {character.heal + character.lucky} health points and take {math.floor((character.defense + character.lucky) / 2)} less damage this round\n"
        return result