"""Basic Flask web chat interface."""

from flask import Flask, request, render_template_string
from chat import generate_response

app = Flask(__name__)

history = []

TEMPLATE = """
<!doctype html>
<title>Chatbot</title>
<h1>Chatbot</h1>
<form method=post>
  <input name=message autofocus>
  <input type=submit value=Send>
</form>
<pre>{{chat}}</pre>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    chat_log = "\n".join(history)
    if request.method == 'POST':
        message = request.form.get('message', '')
        response, _ = generate_response(message, history)
        chat_log = "\n".join(history)
    return render_template_string(TEMPLATE, chat=chat_log)

if __name__ == '__main__':
    app.run(debug=True)
