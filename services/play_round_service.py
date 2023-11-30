import re
import random
import json
from open_ai.open_ai import OpenAI
from database.database import db
from database.models import Character, Game
from rpg_basic_rules import lucky_by_role
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

class PlayRoundService():
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
            "- Develop the opening story for the first round of the RPG, under the title 'The Story:'. "
            "- The scenario involves the players encountering the boss for the first time. "
            "- Include details about the setting, character motivations, mood, and events leading up to the boss confrontation. "
            "- Describe how the players strategize and plan their approach to meet the boss. "
            "- Incorporate tension, character interaction, and potential consequences of their actions. "
            "- Focus on rich storytelling and immersive world-building to set the stage for an engaging RPG experience."
        ) if user_input == "" else (
            "- When receiving user input, start with 'The Story:' and use the input to shape the ongoing narrative. "
            "- The user input is critical in directing the narrative, ensuring it adapts creatively and meaningfully. "
            "- The user input needs to be incorporated into this round and not being a suggestion for the next one."
            "- Maintain continuity and enhance the RPG experience while evolving the narrative based on player decisions. "
            "- Allow for dynamic changes, unexpected plot twists, and character development based on user interactions. "
            "- Ensure the story is a living, evolving tale that reflects the choices and creativity of the players."
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
          - The response begins with 'Game ID:' followed by the ID: {game.game_id}

          The Story:
          - this part should not repeat the context story given, only create the new story for the round
          {context_instructions}
          
          - Feel free to break traditional RPG rules if it enhances the narrative, this could include unexpected plot twists, unique character abilities, or unconventional settings.
          - Ensure that the narrative includes key elements like tension, conflict, and resolution, while developing the characters and the world they inhabit.
          - The story should be dynamic and adjust based on ongoing user inputs, allowing for an interactive and evolving storytelling experience.

          Follow the instructions bellow to guide the attacks:
          {attack_instructions}
          - Damage calculation: Life reduced by damage minus defense. If defense > damage, life unchanged.
          - Announce damage dealt by each character and calculate remaining life.
          - Annouce the remaining life after the damage dealt.
          - Healers can heal one player per round.
          - The boss damages half of the current alive players.
          - If a character's life is lesser than zero it should stay at zero and not be negative; healers cannot revive.
          - <IMPORTANT> After every single attack you must check if the boss or character died (life < 0 or life = 0).</IMPORTANT>
          - Announce when a character dies.
          - if the boss dies, you will ceese the attack and develop the story to its ending.
          
          On Next Round or The End:

          If all of the players and the boss are still alive, life != 0 after the attack, you need to develop the story giving the user 2 different possibilities that the story can have on the next round of the game, be creative and let the story develop in two different ways, for exemple: this could be an unexpected twist, a new strategy that has strengths and weaknesses, a new hidden ability or a powerful artifact that changes the course of battle, presenting new strategic options. this resume should have about 3 lines each, remember to return in a imperative form, using words like will do, insted of could do, this part will start with the title "On Next Round:"

          If all of the players or the boss are dead, life == 0 after the attack, you need to finalize the story, giving the RPG a nice and creative ending, this part will start with the title "The End:", be aware, this part should only be included if all of the players died or the boss is defeated, life == 0.

          - you should not return both of the options on your answer.

          The Characters:

          At the end, you will return all current attributes of every character, make sure to return the proper health attribute after de battle, considering the attacks and heals, like a JSON each, starting with one silge curly brackets for each, this part will start with the title The Characters:
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
            return self.collect_data(answer, game.game_id)
        except Exception as e:
            print(e)
            return { "error": "chat gpt did not respond in correct formart, try again please", "answer": answer.replace("\n", ""), "error_message": str(e) }, 500
    
    def collect_data(self, answer: str, game_id: int):
        answer = answer.replace("\n", "")
        pattern_ending = re.compile(r'(?<=The\sEnd:)[\s\S]*(?=The\sCharacters:)', re.M)
        pattern_round_story = re.compile(r'(?<=The\sStory:)[\s\S]*(?=On\sNext\sRound:|The\sEnd:)', re.M)
        pattern_next_round = re.compile(r'(?<=On\sNext\sRound:)[\s\S]*(?=The\sCharacters:)', re.M)
        pattern_characters = re.compile(r'{[\s\S]*?}', re.M)

        answer_ending = pattern_ending.search(answer)
        answer_round_story = pattern_round_story.search(answer).group()
        next_round_story = pattern_next_round.search(answer)

        characters_data = []
        with Session(db.engine) as session:
            try:
                game_in_session = session.query(Game).get(game_id)

                game_in_session.status = 'finished' if answer_ending else 'on going'
                game_story_updates = [game_in_session.story, answer_round_story]

                if game_in_session.status == 'finished':
                    game_story_updates.append(answer_ending.group())

                game_in_session.story = "\n".join(game_story_updates)

                characters = pattern_characters.findall(answer)
                for character_json in characters:
                    character_data = json.loads(character_json)
                    character_in_db = session.get(Character, character_data["id"])
                    for attr, value in character_data.items():
                        setattr(character_in_db, attr, value)
                    characters_data.append(character_data)

                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error updating characters: {e}")

        return {
            "game_id": game_id,
            "round_story": answer_round_story,
            "on_the_next_round": 'Game Over' if next_round_story is None else next_round_story.group(),
            "ending": 'Game is going' if answer_ending is None else answer_ending.group(),
            "characters": characters_data
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