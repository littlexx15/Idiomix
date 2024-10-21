# NLP-Assessment-24-25
Template repo for the mini-project assessment on the unit IUI000131 Natural Language Processing for the Creative Industries.

For your assessment you should make a new repository based of this template. Your chatbot class should inherit from the base class `ChatbotBase` and you should write new functions that override the basic functions given in this template.

As you develop your own chatbot you should make regular commits using git to track and save the progress of your work. It is a requirement for you to make at **least 3 commits** to show the progress of your work. 

Your submission for the mini-project will be a link to your own git repo that is based of this template class.

### Getting started

Make a new file for your chatbot, e.g. `my_chatbot.py`

In that file you will need to include the line: 
```
import ChatbotBase from chatbot_base
```

In your new file make a new class that inherits from ChatbotBase, e.g.:
```
class MyChatbot(ChatbotBase):
```

The file `run_chatbot.py` should contain the code where your chatbot runs. 

Below is a basic example of what this might look like.

```
from my_chatbot import MyChatbot

if __name__ == "__main__":
    
    chatbot = MyChatbot()
    chatbot.greeting()

    response = chatbot.respond('How are you?')

    while chatbot.conversation_is_active():
        response = chatbot.respond(response)
    
    chatbot.farewell()
```

Your are not limited just to the core functions in the base class ChatbotBase. Feel free to add more functions to your chatbot class if you want your chatbot to have more complex behaviour's or functionality.



