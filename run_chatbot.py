from my_chatbot import MyChatbot

if __name__ == "__main__":
    # Initialize the chatbot
    chatbot = MyChatbot()
    chatbot.greeting()  # Display the initial greeting and rules if requested

    # Main interaction loop
    while chatbot.keep_playing:
        user_input = input("You: ").strip()  # Get input from the user
        chatbot.respond(user_input)  # Process and respond to the input
