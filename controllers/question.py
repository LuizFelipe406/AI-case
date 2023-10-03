from flask_restful import Resource, reqparse
from open_ai.open_ai import OpenAI
from wolfram.wolfram import Wolfram
from . import subjects

class Question(Resource):
    def __init__(self):
        self.open_ai = OpenAI()
        self.wolfram = Wolfram()

    def get(self, subject):
        if subject not in subjects.subjects_allowed:
            return {"message": f"Professor AI is not and expert in {subject}"}, 404

        arguments = reqparse.RequestParser()
        arguments.add_argument('question')

        question = arguments.parse_args()["question"]
        context = f"You are a renowned {subject} teacher, known for your incredible teaching skills and your task is to explain it in a concise way giving examples where appropriate to improve understanding"
        
        # if subject in ["Math", "Chemistry","Physics",]:
        #     return self.wolfram.generate_answer(context, question)

        return self.open_ai.generate_answer(context, question)