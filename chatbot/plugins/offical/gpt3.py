import openai
import os

class Plugin:
    def generator(self, prompt):
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        comp = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt
        )
        return comp.choices[0].text