import os
import openai
import json

class AILibrary:
    def __init__(self):
        API_KEY = os.environ["API_KEY"]
        openai.organization = "org-sUgNqRTwwVZMVytUjb0LYp6b"
        openai.api_key = API_KEY
        openai.Model.list()
    def text(self, prompt):

        interaction = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=500,
        temperature=0
        )
        list = {
          0:interaction["choices"][0]["text"], 
          1:{json.dumps(interaction)}
        }
        return list
