import os

import openai

openai.api_key = os.getenv("OPENAI_NEW_API_KEY")

class OpenAI():
  def generate_answer(self, context, user_input):
    response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
              {
                "role": "system",
                "content": context
              },
              {
                "role": "user",
                "content": str(user_input)
              }
            ],
            temperature=0.7,
            max_tokens=1024
        )
    return response