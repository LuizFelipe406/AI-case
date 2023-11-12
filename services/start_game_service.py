import re
import random
import json
from sqlalchemy import delete
from open_ai.open_ai import OpenAI
from rpg_basic_rules import rpg_roles, rpg_boss
from database.database import db
from database.models import Character, Game

class StartGameService():
  def __init__(self):
        self.open_ai = OpenAI()
  
  def start(self, player_list: list[str]):
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
            - players can have the same type, it shouldn't be unique, but must be choosen randomly
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
        try:
          return self.collect_data(answer, player_list)
        except Exception as e:
          return { "error": "chat gpt did not respond in correct formart, try again please" }, 500
    
  def collect_data(self, answer: str, player_list: list):
        answer = answer.replace("\n", "")
        game = Game(
            game_id=re.search(r'\d{5}', answer, re.M).group(),
            story = re.search(r'(?<=The\sQuest:)[\s\S]*', answer, re.M).group(),
            status='started'
            )

        db.session.add(game)
        db.session.commit()
        
        try:
          characters: list[str] = re.findall(r'{[\s\S]*?}', answer, re.M)
          for i in range(len(player_list) + 1):
              character_dict = json.loads(characters[i])
              character_model = Character(
                game_id=game.game_id,
                role=character_dict["role"],
                type=character_dict["type"],
                name=character_dict["name"],
                life=character_dict["life"],
                defense=character_dict["defense"],
                lucky=character_dict["lucky"],
                attack=character_dict.get("attack", None),
                heal=character_dict.get("heal", None),
              )
              db.session.add(character_model)
        except Exception as e:
            db.session.delete(game)
            db.session.execute(
                delete(Character).where(Character.game_id == game.game_id)
            )
            raise Exception

        db.session.commit()
        return {
            "game_id": game.game_id,
            "characters": characters,
            "story": game.story
        }