import pandas as pd
import random
from chatbot_base import ChatbotBase  # Ensure ChatbotBase is available

class MyChatbot(ChatbotBase):
    def __init__(self, name="Idiomix"):
        super().__init__(name)
        # Load idioms from the CSV file with a relative path
        idioms_df = pd.read_csv('english_idioms.csv')
        self.idioms_list = idioms_df['idioms'].str.strip().str.lower().tolist()  # Convert idioms to lowercase and remove extra spaces
        self.unused_idioms = set(self.idioms_list)  # Track unused idioms

    def greeting(self):
        # Display greeting message
        print(f"Idiomix: Hello! I'm {self.name}. Let's play an idiom relay. You can start by entering any phrase or idiom!")

    def farewell(self):
        # Display farewell message
        print("Idiomix: Hmm, I can't think of any idiom that starts with that letter. I give up!")

    def process_input(self, user_input):
        """Process the player's input to get the last letter."""
        return user_input.strip()[-1].lower() if user_input else None

    def generate_response(self, last_letter):
        """Find a matching idiom that starts with the specified last letter."""
        matching_idioms = [idiom for idiom in self.unused_idioms if idiom.startswith(last_letter)]
        if matching_idioms:
            selected_idiom = random.choice(matching_idioms)
            self.unused_idioms.remove(selected_idiom)  # Remove used idiom from the unused set
            return selected_idiom
        return None

    def respond(self, user_input):
        """Override the respond method to manage interaction flow."""
        last_letter = self.process_input(user_input)
        if last_letter:
            response = self.generate_response(last_letter)
            if response:
                print(f"Idiomix: {response}")
                return response
        # If no matching idiom is found, end the conversation
        self.farewell()
        return None