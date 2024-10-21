"""
Base Chatbot class
Create a new file for your chatbot that inherits from this class
To do this you need to include the following line at the top of your new file:

from chatbot_base import ChatbotBase
"""

class ChatbotBase:
    # Constructor 
    def __init__(self, name="Chatbot"):
        self.name = name
        self.conversation_is_active = True

    # Initial greeting message
    def greeting(self):
        print(f'Hello I am {self.name}')

    # Goodbye message
    def farewell(self):
        print('Goodbye!')
    
    # Return true if conversation is active
    def conversation_is_active(self):
        return self.conversation_is_active

    # Take user input from terminal
    def receive_input(self):
        user_input = input()
        return user_input

    # Take user input and do something with it 
    def process_input(self, user_input):
        raise NotImplementedError('process_input() not implemented in base Chatbot class')

    # Generate a text string and return it
    def generate_response(self, processed_input):
        raise NotImplementedError('generate_response() not implemented in base Chatbot class')

    # Example of main interaction loop 
    # Override this or write other function that handle more complex user interactions
    def respond(self, out_message = None):
        if isinstance(out_message, str): 
            print(out_message)

        received_input = self.receive_input()
        processed_input = self.process_input(received_input)
        response = self.generate_response(processed_input)
        return response
    