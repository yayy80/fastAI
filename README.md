# fastAI

A minimal GPT-2 based chatbot with a simple plugin system. Each response is printed character by character using `textengine.py` and saved to `saved_responses.txt`.

## Usage
1. Clone this repository
2. Run `python chatbot/chat.py`
3. Type a prompt and wait for the generated reply

## Plugins
Plugins live under `chatbot/plugins/`. When `chat.py` starts it automatically loads any Python file in that directory (recursively) that defines a `Plugin` class. If the class provides a `generator(prompt)` method, its output will be printed alongside the main GPT-2 response.

To create a plugin:

```python
# chatbot/plugins/my_plugin.py
class Plugin:
    def generator(self, prompt):
        return "Custom response"
```

Simply place the file in the plugins folder and run `chat.py` again. The plugin will be discovered automatically. See `chatbot/plugins/offical/gpt3.py` for a more detailed example that calls the OpenAI API.
