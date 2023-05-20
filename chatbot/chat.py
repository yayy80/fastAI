from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from textengine import TextEngine
from chatbot.plugins.offical import gpt3

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')

# Set up the text generation pipeline
text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

# Generate some text
text = input("Message: ")
prompt = f"Guiding Prompt: You are a helpful assistant trained by OpenAI. Your goal is to provide appropriate and helpful responses based on the user's input. Do not guess what the user is going to say, and avoid adding other bots to the conversation, unless the user specifically requests it by including the text ""/more_ai" " in their input. Your responses should be concise and to the point, but also friendly and natural-sounding. Keep in mind that while the maximum number of tokens per response is set to 1000, it is generally better to keep your responses shorter than that, as long responses may be less engaging for the user\nUser: " + text + "\nBot:"
text_gen = text_generator(prompt, max_length=1000, num_return_sequences=1)[0]['generated_text']
# Save the generated response
with open('saved_responses.txt', 'a') as f:
    f.write(text_gen + '\n')

txteng = TextEngine.textengine

gpt_3_gen = gpt3.Plugin.generator

txteng(text_gen)
txteng(gpt_3_gen(prompt=prompt))