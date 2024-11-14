from my_chatbot import MyChatbot

if __name__ == "__main__":
    # Initialize the chatbot
    chatbot = MyChatbot()
    chatbot.greeting()  # Initial greeting message

    # Main interaction loop
    while chatbot.conversation_is_active:
        user_input = input("You: ")
        chatbot.respond(user_input)  # Process and respond to user input

    print("Chatbot: Goodbye! Thanks for playing!")
