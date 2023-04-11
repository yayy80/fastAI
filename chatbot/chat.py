from flask import Flask, render_template, request, session, redirect, url_for
from textengine import TextEngine
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')

# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        if request.method == 'POST':
            # Get user input
            user_input = request.form['user_input']

            # Set up the text generation pipeline
            text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

            # Generate some text
            prompt = f"Guiding Prompt: You are a helpful assistant trained by OpenAI. Your goal is to provide appropriate and helpful responses based on the user's input. Do not guess what the user is going to say, and avoid adding other bots to the conversation, unless the user specifically requests it by including the text ""/more_ai" " in their input. Your responses should be concise and to the point, but also friendly and natural-sounding. Keep in mind that while the maximum number of tokens per response is set to 1000, it is generally better to keep your responses shorter than that, as long responses may be less engaging for the user\nUser: " + user_input + "\nBot:"
            text_gen = text_generator(prompt, max_length=1000, num_return_sequences=1)[0]['generated_text']

            # Save conversation to file
            with open('saved_conversations.txt', 'a') as f:
                f.write(user_input + "\n")
                f.write(text_gen + "\n")

            # Return generated text to user
            return render_template('index.html', text=TextEngine.textengine(text_gen))
        else:
            return render_template('index.html')
    else:
        return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if username and password are correct
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid login credentials')
    else:
        return render_template('login.html')

# Logout page
@app.route('/logout')
def logout():
    # Clear session data
    session.pop('username', None)
    return redirect(url_for('login'))

# Saved conversations page
@app.route('/saved_conversations')
def saved_conversations():
    # Load saved conversations from file
    with open('saved_conversations.txt', 'r') as f:
        conversations = f.readlines()

    # Combine user and bot messages into conversation pairs
    conversation_pairs = [(conversations[i], conversations[i+1]) for i in range(0, len(conversations), 2)]

    return render_template('saved_conversations.html', conversation_pairs=conversation_pairs)

if __name__ == '__main__':
    app.run(debug=True)
