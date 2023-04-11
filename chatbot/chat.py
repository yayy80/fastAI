from flask import Flask, render_template, request, redirect, session
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from textengine import TextEngine

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')

# Home page
@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html')
    else:
        return redirect('/login')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        if user == 'admin' and password == 'password':
            session['user'] = user
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        # Implement your own user registration logic here
        return redirect('/login')
    else:
        return render_template('signup.html')

# Saved conversations page
@app.route('/conversations')
def conversations():
    if 'user' in session:
        with open('saved_responses.txt', 'r') as f:
            conversations = f.readlines()
        return render_template('conversations.html', conversations=conversations)
    else:
        return redirect('/login')

# Chat page
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user' in session:
        # Set up the text generation pipeline
        text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
        if request.method == 'POST':
            text = request.form['text']
            # Generate some text
            prompt = f"Guiding Prompt: You are a helpful assistant trained by OpenAI. Your goal is to provide appropriate and helpful responses based on the user's input. Do not guess what the user is going to say, and avoid adding other bots to the conversation, unless the user specifically requests it by including the text ""/more_ai" " in their input. Your responses should be concise and to the point, but also friendly and natural-sounding. Keep in mind that while the maximum number of tokens per response is set to 1000, it is generally better to keep your responses shorter than that, as long responses may be less engaging for the user\nUser: " + text + "\nBot:"
            text_gen = text_generator(prompt, max_length=1000, num_return_sequences=1)[0]['generated_text']
            # Save the generated response
            with open('saved_responses.txt', 'a') as f:
                f.write(text_gen + '\n')
            return render_template('chat.html', text=text, response=text_gen)
        else:
            return render_template('chat.html')
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

