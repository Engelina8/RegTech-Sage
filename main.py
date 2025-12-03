from chatbot import RegTechSageChatbot

def main():
    bot = RegTechSageChatbot()
    print("RegTech Sage: Regulatory Compliance Chatbot\nType 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        try:
            response = bot.ask(user_input)
            print(f"RegTech Sage: {response}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
