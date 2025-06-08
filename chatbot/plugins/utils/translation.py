from transformers import pipeline

class Plugin:
    def __init__(self):
        self.translator_en = pipeline('translation', model='t5-small')

    def generator(self, prompt):
        return self.translator_en(prompt)[0]['translation_text']
