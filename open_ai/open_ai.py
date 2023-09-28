import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAI():
  def generate_answer(self, context, question):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
              {
                "role": "system",
                "content": context
              },
              {
                "role": "user",
                "content": question
              }
            ],
            temperature=0.1,
            max_tokens=1024
        )
    return response