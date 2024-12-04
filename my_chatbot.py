import pandas as pd
import random
import spacy
import re
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
        self.score = 0  # Initialize the score counter

    def greeting(self):
        """Send a greeting to the user and ask if they want to hear the game rules."""
        print(f"Idiomix: Hi! Welcome to the Idiomix Game!")
        self.ask_game_rules()

    def farewell(self):
        """Send a farewell message and end the game with score and rating."""
        print("Idiomix: Thanks for playing! Here's how you did:")
        print(f"Idiomix: Your total score is: {self.score}")
        rating = self.calculate_rating()
        print(f"Idiomix: {rating}")

    def ask_game_rules(self):
        """Display the game rules or skip to starting the game."""
        print("Idiomix: Do you want to know the rules? ")
        user_response = input("You: ").strip().lower()
        if user_response in ["yes", "sure", "yeah", "of course"]:
            print(
                "Idiomix: Here's how we play:\n"
                "- Type an idiom or phrase, and I'll respond with one that starts with the last letter of yours.\n"
                "- If you're unsure, type 'hint' for a clue, or 'skip' to pass.\n"
                "- You can also ask me to explain the meaning of any idiom I use!\n"
                "- Every correct idiom earns you a point, and your final score will give you a rating.\n"
                "Ready to test your idiom skills? Let's begin!"
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
        - Utilizes regex for improved detection accuracy.
        """
        emotional_patterns = {
            "positive": r"\b(love|like|enjoy|funny|interesting)\b",
            "negative": r"\b(hate|dislike|annoyed|bored|boring|frustrating)\b"
        }
        target_patterns = r"\b(you|this game|chatbot|conversation|the game)\b"

        user_input_lower = user_input.lower()

        for sentiment, emotion_pattern in emotional_patterns.items():
            if re.search(emotion_pattern, user_input_lower):
                if re.search(target_patterns, user_input_lower):
                    return sentiment
        return None

    def handle_emotion_response(self, sentiment):
        """
        Respond to emotional feedback and decide whether to continue or end the game.
        """
        if sentiment == "negative":
            print("Idiomix: Oh no, I'm sorry you feel that way. Want to try another round?")
            user_response = input("You: ").strip().lower()
            if user_response in ["yes", "sure", "yeah", "of course"]:
                print("Idiomix: Great! Let's keep playing!")
                return True
            else:
                self.farewell()
                return False
        elif sentiment == "positive":
            print("Idiomix: Aww, that's so kind of you! Thank you! Let's keep playing!")
            return True

    def process_input(self, user_input, required_letter=None):
        """
        Process user input:
        - Handle 'hint' or 'skip' commands
        - Check for exit requests
        - Handle explanation requests
        - Detect emotional expressions
        - Validate if input is a valid idiom
        """
        if not user_input.strip():
            print("Idiomix: Hmm, I didn't hear anything. Try typing something!")
            return None

        sentiment = self.detect_emotional_target(user_input)
        if sentiment:
            self.keep_playing = self.handle_emotion_response(sentiment)
            return None

        if re.search(r"(how to|what should|hint|help me|can you help)", user_input.lower()):
            return "hint"

        if re.search(r"(skip|change|move on|can we change)", user_input.lower()):
            return "skip"

        if re.search(r"(quit|give up|stop playing|want to end|leave)", user_input.lower()):
            self.farewell()
            self.keep_playing = False
            return None

        if re.search(r"(explain|define|meaning|what does|what is|what's that)", user_input.lower()):
            self.explain_idiom()
            return None

        is_valid_idiom = self.check_user_input(user_input, required_letter)
        if not is_valid_idiom:
            return None
        return user_input.strip()[-1].lower()

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

    def calculate_rating(self):
        """Calculate the rating based on the score."""
        if self.score <= 2:
            return "Beginner player! Keep trying and learn more idioms."
        elif 3 <= self.score <= 5:
            return "Skilled player! You're getting the hang of idioms."
        elif 6 <= self.score <= 9:
            return "Excellent player! You're an idiom master."
        else:
            return "Grandmaster player! Your idiom skills are unbeatable!"

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
                    self.score += 1
                    print(f"Idiomix: {response}")
                    user_input = input("You: ").strip()
                else:
                    print("Idiomix: Hmm, I can't think of one. You win!")
                    self.farewell()
                    self.keep_playing = False
            else:
                user_input = input("You: ").strip()
