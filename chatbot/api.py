"""Flask API to interact with the chatbot programmatically."""

from flask import Flask, request, jsonify
from chat import generate_response

app = Flask(__name__)

history = []

@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.get_json() or {}
    message = data.get('message', '')
    response, _ = generate_response(message, history)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
