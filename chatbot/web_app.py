"""Basic Flask web chat interface."""

from flask import Flask, request, render_template

from chat import generate_response

app = Flask(__name__)

history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    chat_log = "\n".join(history)
    if request.method == 'POST':
        message = request.form.get('message', '')
        response, _ = generate_response(message, history)
        chat_log = "\n".join(history)
    return render_template('index.html', chat=chat_log)

if __name__ == '__main__':
    app.run(debug=True)
