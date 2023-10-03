import os
from requests import request


wolfram_id = os.getenv("WOLFRAM_API_KEY")

class Wolfram():
  def generate_answer(self, context: str, question: str):
    input = (question).replace(" ", "+")
    print(input)
    wolfram_url = f"http://api.wolframalpha.com/v1/conversation.jsp?appid={wolfram_id}&i={input}"
    response = request("get", wolfram_url)
    return response.json()