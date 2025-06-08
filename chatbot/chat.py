"""Main chat loop supporting plugins, basic NLU, conversation memory and optional voice."""

import os
from pathlib import Path
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from textengine import TextEngine
from plugin_loader import discover_plugins

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover - optional
    sr = None

try:
    import pyttsx3
except Exception:  # pragma: no cover - optional
    pyttsx3 = None

# initialize models
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')
text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
nlu = pipeline('sentiment-analysis')

# optional text-to-speech
tts_engine = pyttsx3.init() if pyttsx3 else None

# helpers
plugins = discover_plugins()
txteng = TextEngine.textengine

def get_user_input():
    if os.environ.get('VOICE_MODE') and sr:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            txteng('Listening...')
            audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except Exception:
            return input('Message: ')
    return input('Message: ')


def speak(text: str):
    if tts_engine:
        tts_engine.say(text)
        tts_engine.runAndWait()


def save_feedback(prompt: str, response: str):
    rating = input('Rate response 1-5 (or Enter to skip): ')
    if rating:
        with open('feedback.txt', 'a') as fb:
            fb.write(f'Prompt: {prompt}\nResponse: {response}\nRating: {rating}\n---\n')


def generate_response(user_text: str, history: list):
    """Generate a response given a user message and conversation history."""
    sentiment = nlu(user_text)[0]['label']
    history.append(f'User: {user_text}')

    prompt = (
        'Guiding Prompt: You are a helpful assistant. Consider the conversation\n'
        + '\n'.join(history)
        + f"\nSentiment:{sentiment}\nBot:"
    )


    text_gen = text_generator(prompt, max_length=200, num_return_sequences=1)[0]['generated_text']
    history.append(f'Bot: {text_gen}')

    with open('saved_responses.txt', 'a') as f:
        f.write(text_gen + '\n')

    return text_gen, prompt


def main():
    history = []
    while True:
        user_text = get_user_input()
        if user_text.lower() in {'exit', 'quit'}:
            break

        text_gen, prompt = generate_response(user_text, history)

        txteng(text_gen)
        speak(text_gen)

        for plugin in plugins.values():
            plugin_cls = getattr(plugin, 'Plugin', None)
            if plugin_cls and hasattr(plugin_cls, 'generator'):
                generator = plugin_cls().generator
                txteng(generator(prompt=prompt))

        save_feedback(user_text, text_gen)


if __name__ == '__main__':
    main()
