import re
import random
import json
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

        context_instructions = (
            '- Develop the opening story for the first round of the RPG, under the title "The Story:". '
            '- In this scenario, players are encountering the boss for the first time. Craft a narrative that encompasses more than the initial attack. '
            '- Detail the events leading up to this confrontation, including the setting, character motivations, and the mood. '
            '- Describe how the players come to meet the boss, including any strategy or planning they may have done. '
            '- Incorporate elements of tension, character interaction, and potential consequences of their actions. '
            '- This part of the story should set the stage for an engaging RPG experience, with a focus on rich storytelling and immersive world-building.'
        ) if user_input == "" else (
            '- When receiving user input, use it to shape the ongoing story, starting with "The Story:". '
            '- The user input is pivotal in directing the narrative. Ensure that the story adapts to incorporate these inputs creatively and meaningfully. '
            '- The narrative should evolve based on what the players decide or describe, with a focus on maintaining continuity and enhancing the RPG experience. '
            '- Be flexible in how the story unfolds, allowing for dynamic changes, unexpected plot twists, and character development based on user interactions. '
            '- The story should be more than just an account of events; it should be a living, evolving tale that reflects the choices and creativity of the players.'
)

        attack_instructions = self.calculate_attack(characters)
        context = f"""
          You are an experienced RPG master, capable of creating the best storys, twists and surprises, this time you will be mastering a round of the game.
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
          - this part should not repeat the context story given, only create the new story for the round
          {context_instructions}
          
          - Feel free to break traditional RPG rules if it enhances the narrative, this could include unexpected plot twists, unique character abilities, or unconventional settings.
          - Ensure that the narrative includes key elements like tension, conflict, and resolution, while developing the characters and the world they inhabit.
            
            The story should be dynamic and adjust based on ongoing user inputs, allowing for an interactive and evolving storytelling experience.
          Follow the instructions bellow to guide the attacks:
          {attack_instructions}
          - the life is reduced according to the damage minus the defense of the person being attacked
          - if the defense is greater than the damage, the life is not changed
          - you need to calculate the life remaining of the defender after each character attack
          - You need to announce how much damage each character did after they're attack
          - the healer can only heal one player per round.
          - the boss will damage half of the current alive players
          - if a character gets a life lesser than zero, the life will stay at zero and should not be negative.
          - a healer cannot revive a character, once his life gets to zero, he cannot heal that character anymore.
          - you must announce whenever a character dies, wich means, his life is reduced to zero
          
          On Next Round/The End:

          If all of the players and the boss are still alive, life != 0 after the attack, you need to develop the story giving the user 2 different possibilities that the story can have on the next round of the game, be creative and let the story develop in two different ways, this could be an unexpected twist, a new hidden ability or a powerful artifact that changes the course of battle, presenting new strategic options, this resume should have about 3 lines each,remember to return in a imperative form, using words like will do, insted of could do, this part will start with the title "On Next Round:"

          If all of the players or the boss are dead, life == 0 after the attack, you need to finalize the story, giving the RPG a nice and creative ending, this part will start with the title "The End:", be aware, this part should only be included if all of the players died or the boss is defeated, life == 0.

          The Characters:

          At the end, you will return all current attributes of every character, make sure to return the proper health attribute after de battle, like a JSON each, starting with one silge curly brackets for each, this part will start with the title The Characters:
          example:
           {{
              "id": xxxx,
	          "role": "xxxx",
              "type": "xxxx",
	          "name": "xxxx",
              "action": xxxx,
	          "life": xxxx,
	          "defense": xxxx,
	          "lucky": xxxx
            }}  
"""
        response = self.open_ai.generate_answer(context, user_input)
        answer = response.choices[0].message.content
        try:
            return self.collect_data(answer, game, user_input)
        except Exception as e:
            print(e)
            return { "error": "chat gpt did not respond in correct formart, try again please", "answer": answer.replace("\n", ""), "error_message": str(e) }, 500
    
    def collect_data(self, answer: str, game: Game, user_input):
        answer = answer.replace("\n", "")
        answer_ending = re.search(r'(?<=The\sEnd:)[\s\S]*(?=The\sCharacters:)', answer, re.M)
        answer_round_story = re.search(r'(?<=The\sStory:)[\s\S]*(?=On\sNext\sRound:|The\sEnd:)', answer, re.M).group()
        next_round_story = re.search(r'(?<=On\sNext\sRound:)[\s\S]*(?=The\sCharacters:)', answer, re.M)

        game.status = 'on going' if answer_ending is None else 'finished'
        game.story = game.story + "\n" + answer_round_story
        
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
            raise e
        db.session.commit()
        return {
            "game_id": game.game_id,
            "characters": characters,
            "full_story": game.story,
            "round_story": answer_round_story,
            "on_the_next_round": 'Game Over' if next_round_story is None else next_round_story.group(),
            "ending": 'Game is going' if answer_ending is None else answer_ending.group(),
            "full_answer": answer,
            "user_input_sent": user_input
        }
    
    def calculate_lucky(self, character: Character):
        character_lucky_min = lucky_by_role[character.role][0]
        character_lucky_max = lucky_by_role[character.role][1]
        return random.randint(character_lucky_min, character_lucky_max)
       

    def calculate_attack(self, characters: list[Character]):
        healer_char = [char for char in characters if char.role == 'Healer']
        non_healer_chars = [char for char in characters if char.role != 'Healer']

        random.shuffle(non_healer_chars)

        reordered_characters = non_healer_chars + healer_char

        result = "the order of the attack will be: \n"

        for index, character in enumerate(reordered_characters):
            if character.life > 0:
                action_word = 'deal' if character.role != 'Healer' else 'give'
                points_word = 'damage' if character.role != 'Healer' else 'health points'
                points = character.action + character.lucky
                result += f"{index + 1}- the character {character.name} will {action_word} {points} {points_word} this round\n"
        return result