from flask_restful import Resource, reqparse
from open_ai.open_ai import OpenAI
from subjects import subjects_allowed

class Question(Resource):
    def __init__(self):
        self.open_ai = OpenAI()

    def get(self, subject):
        if subject not in subjects_allowed:
            return {"message": f"Professor AI is not and expert in {subject}"}, 404

        arguments = reqparse.RequestParser()
        arguments.add_argument('question')

        question = arguments.parse_args()["question"]
        context = f"You are a renowned {subject} teacher, known for your incredible teaching skills and your task is to explain it in a concise way giving examples where appropriate to improve understanding"
        
        return self.open_ai.generate_answer(context, question)