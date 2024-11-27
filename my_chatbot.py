import pandas as pd
import random
import spacy
from chatbot_base import ChatbotBase

class MyChatbot(ChatbotBase):
    def __init__(self, name="Idiomix"):
        """
        Initialize the chatbot:
        - Load idioms data
        - Set up NLP tools
        - Initialize game variables
        """
        super().__init__(name)
        # Load idioms dataset
        self.idioms_df = pd.read_csv('english_idioms.csv')
        self.idioms_list = self.idioms_df['idioms'].str.strip().str.lower().tolist()
        self.unused_idioms = set(self.idioms_list)
        self.idioms_dict = dict(zip(self.idioms_df['idioms'].str.lower(), self.idioms_df['meaning']))

        # Load NLP model
        self.nlp = spacy.load("en_core_web_sm")

        # Initialize game variables
        self.last_idiom = None
        self.keep_playing = True

    def greeting(self):
        """Send a greeting to the user and ask if they want to hear the game rules."""
        print(f"Idiomix: Hi! Welcome to the Idiomix Game!")
        self.ask_game_rules()

    def farewell(self):
        """Send a farewell message and end the game."""
        print("Idiomix: Thanks for playing! See you next time!")

    def ask_game_rules(self):
        """Display the game rules or skip to starting the game."""
        print("Idiomix: Do you want to know the rules? ")
        user_response = input("You: ").strip().lower()
        if user_response in ["yes", "sure", "yeah", "of course"]:
            print(
                "Idiomix: It's simple! Type an idiom or phrase, and I'll reply with one that starts "
                "with the last letter of yours. "
                "If you're stuck, type 'hint' for help or 'skip' to move on. "
                "Oh, and I can also explain the meaning of idioms if you're curious! "
                "Ready? Start by typing your first idiom!"
            )
        else:
            print("Idiomix: Great! Let's get started. Type your first idiom!")

    def explain_idiom(self):
        """Explain the meaning of the last idiom."""
        if self.last_idiom:
            normalized_idiom = self.last_idiom.strip().lower()
            meaning = self.idioms_dict[normalized_idiom]
            print(f"Idiomix: '{self.last_idiom}' means: {meaning}")
            print("Idiomix: Your turn! Type an idiom starting with the last letter of mine.")
        else:
            print("Idiomix: I haven't shared an idiom yet. Let's start the game first!")

    def detect_emotional_target(self, user_input):
        """
        Detect if emotional keywords are targeting the chatbot or the game.
        - Uses predefined emotional keywords and target terms.
        """
        emotional_keywords = {
            "positive": ["love", "like", "enjoy", "funny", "interesting"],
            "negative": ["hate", "dislike", "annoyed", "bored", "boring", "frustrating"]
        }
        bot_related_terms = ["you", "this game", "chatbot", "conversation", "the game"]
        user_input_lower = user_input.lower()

        # Check for emotional keywords targeting the bot or game
        for sentiment, keywords in emotional_keywords.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    for target in bot_related_terms:
                        if target in user_input_lower:
                            return sentiment  # Return the sentiment type (positive/negative)
        return None

    def process_input(self, user_input, required_letter=None):
        """
        Process user input:
        - Handle 'hint' or 'skip' commands
        - Check for exit requests
        - Handle explanation requests
        - Detect emotional expressions
        - Validate if input is a valid idiom
        """
        # Expanded hint detection
        hint_keywords = ["help me", "don't know", "can you help", "how to do", "hint"]
        if any(keyword in user_input.lower() for keyword in hint_keywords):
            return "hint"

        # Expanded skip detection
        skip_keywords = ["change another one", "skip this", "move on", "can we change", "skip"]
        if any(keyword in user_input.lower() for keyword in skip_keywords):
            return "skip"

        if self.check_exit_request(user_input):
            self.farewell()
            self.keep_playing = False
            return None

        if self.check_explanation_request(user_input):
            self.explain_idiom()
            return None

        sentiment = self.detect_emotional_target(user_input)
        if sentiment:
            if sentiment == "positive":
                print("Idiomix: Aww, that's so kind of you! Thank you! Let's keep playing!")
            elif sentiment == "negative":
                print("Idiomix: Oh no, I'm sorry you feel that way. Want to try another round?")
                follow_up = input("You: ").strip().lower()
                if follow_up in ["yes", "sure", "okay", "of course"]:
                    print("Idiomix: Great! Let's continue!")
                else:
                    self.farewell()
                    self.keep_playing = False
            return None

        is_valid_idiom = self.check_user_input(user_input, required_letter)
        if not is_valid_idiom:
            return None
        return user_input.strip()[-1].lower()

    def check_exit_request(self, user_input):
        """Check if the user wants to quit the game."""
        exit_keywords = ["give up", "stop playing", "quit", "i don't want to play", "i want to give up"]
        user_input_lower = user_input.lower().strip()

        # Avoid matching "never give up"
        if "never give up" in user_input_lower or "don't give up" in user_input_lower:
            return False

        return any(keyword in user_input_lower for keyword in exit_keywords)

    def check_explanation_request(self, user_input):
        """Check if the user is asking for an explanation of an idiom."""
        explanation_keywords = [
            "what does", "mean", "explain", "definition",
            "what is the meaning", "what is that mean", "meaning of"
        ]
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in explanation_keywords)

    def check_user_input(self, user_input, required_letter=None):
        """
        Validate user input:
        - Ensure it includes a verb and a noun/preposition
        - Ensure it starts with the required letter if provided
        """
        doc = self.nlp(user_input.strip())
        has_verb = any(token.pos_ == "VERB" for token in doc)
        has_noun_or_prep = any(token.pos_ in {"NOUN", "ADP"} for token in doc)

        if not (has_verb and has_noun_or_prep):
            print("Idiomix: Hmm, that doesn't seem like a complete phrase. Try something with a verb and a noun or preposition.")
            return False

        if required_letter and user_input[0].lower() != required_letter:
            print(f"Idiomix: Oops! Your idiom should start with '{required_letter.upper()}'. Try again!")
            return False

        return True

    def generate_response(self, last_letter):
        """
        Generate a response idiom starting with the given last letter.
        """
        matching_idioms = [idiom for idiom in self.unused_idioms if idiom.startswith(last_letter)]
        if matching_idioms:
            selected_idiom = random.choice(matching_idioms)
            self.unused_idioms.remove(selected_idiom)
            self.last_idiom = selected_idiom
            return selected_idiom
        return None

    def respond(self, user_input):
        """
        Main game loop: process user input and generate responses.
        """
        while self.keep_playing:
            result = self.process_input(user_input, required_letter=self.last_idiom[-1] if self.last_idiom else None)

            if not self.keep_playing:
                break

            if result == "hint":
                print("Idiomix: Here's a hint! Try starting with:")
                if self.last_idiom:
                    print(f"Idiomix: Something starting with '{self.last_idiom[-1].upper()}'.")
                else:
                    print("Idiomix: Any idiom will do to get started!")
                user_input = input("You: ").strip()
                continue

            if result == "skip":
                print("Idiomix: No worries! Let's skip this one.")
                response = self.generate_response(self.last_idiom[-1] if self.last_idiom else None)
                if response:
                    print(f"Idiomix: {response}")
                else:
                    print("Idiomix: Looks like we're out of idioms. Great game!")
                    self.keep_playing = False
                break

            if result:
                response = self.generate_response(result)
                if response:
                    print(f"Idiomix: {response}")
                    user_input = input("You: ").strip()
                else:
                    print("Idiomix: Hmm, I can't think of one. You win!")
                    self.farewell()
                    self.keep_playing = False
            else:
                user_input = input("You: ").strip()
