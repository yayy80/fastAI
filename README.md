# fastAI
A GPT-2 implementation with no OpenAI API key 🎉🎉🎉, that acts like a chatbot (similar to AutoGPT and gpt4all)

## Examples:
- What are burritos?
- Write a python script that prints "Hello, World!"

---------------
# Usage:
1. Clone this repository
2. Run "cd chatbot"
3. Run "python chat.py"
4. Wait, then type something
5. Wait for it to finish
6. You will see "textengine.py" in action
7. Wait for it to finish, and see it appear in "saved_responses.txt"

---------------
# Plugin Usage
1. Clone this repository
2. Run "cd chatbot"
3. Run "cd plugins"
4. Create a new folder called your plugins name
5. Your plugin would look like: 
```
class Plugin:
    def __init__(self): # if the __ __ is disapeared and its bold, its because of markdown formatting.
        self.tasks = []

    def add_task(self, task_name):
        self.tasks.append(task_name)

    def remove_task(self, task_name):
        self.tasks.remove(task_name)

    def list_tasks(self):
        return self.tasks
```
6. To implement that plugin, modify chat.py as follows: 
```
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from textengine import TextEngine
from chatbot.plugins.offical import gpt3
from chatbot.plugins.todo import todo.py

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')

# Set up the text generation pipeline
text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

# Instantiate the To-Do plugin
todo_plugin = Plugin()

# Generate some text
text = input("Message: ")

# Check if the user wants to add a task
if text.startswith("add task"):
    task_name = text[9:].strip()  # Extract the task name from the user input
    todo_plugin.add_task(task_name)
    print("Task added successfully.")

# Check if the user wants to list tasks
elif text == "list tasks":
    tasks = todo_plugin.list_tasks()
    print("Tasks:")
    for task in tasks:
        print(task)

# Handle other user inputs as before
else:
    prompt = f"Guiding Prompt: You are a helpful assistant trained by OpenAI. Your goal is to provide appropriate and helpful responses based on the user's input. Do not guess what the user is going to say, and avoid adding other bots to the conversation, unless the user specifically requests it by including the text ""/more_ai" " in their input. Your responses should be concise and to the point, but also friendly and natural-sounding. Keep in mind that while the maximum number of tokens per response is set to 1000, it is generally better to keep your responses shorter than that, as long responses may be less engaging for the user\nUser: " + text + "\nBot:"
    text_gen = text_generator(prompt, max_length=1000, num_return_sequences=1)[0]['generated_text']
    # Save the generated response
    with open('saved_responses.txt', 'a') as f:
        f.write(text_gen + '\n')

    txteng = TextEngine.textengine

    gpt_3_gen = gpt3.Plugin.generator

    txteng(text_gen)
    txteng(gpt_3_gen(prompt=prompt))
```
