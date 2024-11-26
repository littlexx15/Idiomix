import pandas as pd
import random
import spacy
from chatbot_base import ChatbotBase

class MyChatbot(ChatbotBase):
    def __init__(self, name="Idiomix"):
        super().__init__(name)
        # Load idioms from the CSV file with a relative path
        idioms_df = pd.read_csv('english_idioms.csv')
        self.idioms_list = idioms_df['idioms'].str.strip().str.lower().tolist()  # Convert idioms to lowercase and remove extra spaces
        self.unused_idioms = set(self.idioms_list)  # Track unused idioms

        # Load spaCy language model for NLP
        self.nlp = spacy.load("en_core_web_sm")

    def greeting(self):
        print(f"Idiomix: Hello! I'm {self.name}. Let’s play an idiom relay game! Start by typing an idiom!")

    def farewell(self):
        print("Idiomix: Hmm, I can't think of any idiom that starts with that letter. I give up!")

    def is_possible_idiom(self, user_input):
        """
        Check if input matches idiomatic patterns like 'verb + noun' or 'verb + prepositional phrase'.
        """
        doc = self.nlp(user_input.strip())
        has_verb = any(token.pos_ == "VERB" for token in doc)
        has_noun_or_prep = any(token.pos_ in {"NOUN", "ADP"} for token in doc)
        return has_verb and has_noun_or_prep  # Ensure the input has both verb and noun/preposition

    def process_input(self, user_input):
        """Process input if it appears to be an idiom."""
        if self.is_possible_idiom(user_input):
            # Return the last letter of the input if it matches idiomatic patterns
            return user_input.strip()[-1].lower()
        else:
            # Friendly prompt for non-idiomatic input
            print("Idiomix: Hmm, that doesn’t seem like a common idiom! Try another one.")
            return None

    def generate_response(self, last_letter):
        """Find a matching idiom that starts with the given last letter."""
        matching_idioms = [idiom for idiom in self.unused_idioms if idiom.startswith(last_letter)]
        if matching_idioms:
            selected_idiom = random.choice(matching_idioms)
            self.unused_idioms.remove(selected_idiom)
            return selected_idiom
        return None

    def respond(self, user_input):
        """Main loop to handle user input and respond accordingly."""
        while True:
            last_letter = self.process_input(user_input)
            if last_letter:
                response = self.generate_response(last_letter)
                if response:
                    print(f"Idiomix: {response}")
                    user_input = input("You: ").strip()  # Continue to prompt the user for more input
                else:
                    self.farewell()
                    break
            else:
                # If input doesn't seem like an idiom, prompt the user again
                user_input = input("You: ").strip()
