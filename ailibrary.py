import os
import openai
import json

class AILibrary:
    def __init__(self):
        API_KEY = os.environ["API_KEY"]
        openai.organization = "org-sUgNqRTwwVZMVytUjb0LYp6b"
        openai.api_key = API_KEY
        openai.Model.list()
    def debug(self, prompt):
      response = openai.Completion.create(
      model="code-davinci-002",
      prompt=f"##### Fix bugs in the below function\n \n### Buggy Python\n{prompt}\n### Fixed Python",
      temperature=0,
      max_tokens=500,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=["###"]
            
      )
      list = {
          0:interaction["choices"][0]["text"], 
          1:{json.dumps(interaction)},
          2:interaction["choices"][0]["finish_reason"]
        }
      return list

    def text(self, prompt, model):
        model3 = model
        interaction = openai.Completion.create(
        model=model3,
        prompt=prompt,
        max_tokens=900,
        temperature=0
        )
        list = {
          0:interaction["choices"][0]["text"], 
          1:{json.dumps(interaction)},
          2:interaction["choices"][0]["finish_reason"]
        }
        return list
