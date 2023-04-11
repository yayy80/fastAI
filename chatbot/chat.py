from textengine import TextEngine
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import os

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')

# Define a list to store generated responses
responses = []

def gen():
    global responses
    text = input("> ")

    # Check if user requested to see previous responses
    if text.strip() == '/saved_responses':
        for i, resp in enumerate(responses):
            print(f'{i + 1}. {resp}')
        return

    # Set up the text generation pipeline
    text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

    # Generate some text
    prompt = f"Guiding Prompt: You are a helpful assistant trained by OpenAI. Your goal is to provide appropriate and helpful responses based on the user's input. Do not guess what the user is going to say, and avoid adding other bots to the conversation, unless the user specifically requests it by including the text ""/more_ai" " in their input. Your responses should be concise and to the point, but also friendly and natural-sounding. Keep in mind that while the maximum number of tokens per response is set to 1000, it is generally better to keep your responses shorter than that, as long responses may be less engaging for the user\nUser: " + text + "\nBot:"
    text_gen = text_generator(prompt, max_length=1000, num_return_sequences=1)[0]['generated_text']

    # Add generated response to the list
    responses.append(text_gen)

    # Remove the prompt from the generated text
    text_gen = text_gen.replace(prompt, '').strip()

    # Display the generated text to the user
    TextEngine.textengine(text=text_gen)

    # Write the generated text to the file: saved_responses.txt
    with open('saved_responses.txt', 'a') as f:
        # Write the generated text
        f.write(text_gen + '\n')

while True:
    try:
        gen()
    except Exception as e:
        print("Error: " + str(e))