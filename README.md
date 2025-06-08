# fastAI

A minimal GPT-2 based chatbot with a simple plugin system. Each response is printed character by character using `textengine.py` and saved to `saved_responses.txt`. The bot now includes rudimentary natural language understanding, optional voice input/output, conversation memory and a feedback system.

## Usage
1. Clone this repository
2. Run `python chatbot/chat.py`
3. Type a prompt and wait for the generated reply
### Web and API
Run `python chatbot/api.py` to start a simple JSON API or `python chatbot/web_app.py` for a minimal web chat interface.

## Plugins
Plugins live under `chatbot/plugins/`. When `chat.py` starts it automatically loads any Python file in that directory (recursively) that defines a `Plugin` class. If the class provides a `generator(prompt)` method, its output will be printed alongside the main GPT-2 response. Example plugins include a GPT-3 wrapper and a translation plugin.

To create a plugin:

```python
# chatbot/plugins/my_plugin.py
class Plugin:
    def generator(self, prompt):
        return "Custom response"
```

Simply place the file in the plugins folder and run `chat.py` again. The plugin will be discovered automatically. See `chatbot/plugins/offical/gpt3.py` for a more detailed example that calls the OpenAI API.


### Multi-language
The bot uses a simple translation plugin to demonstrate multi-language support. Enable it by placing a plugin like `chatbot/plugins/utils/translation.py` in the plugins folder.
