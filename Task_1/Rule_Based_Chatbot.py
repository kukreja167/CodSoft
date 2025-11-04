# ------------------------------------------------------------
# Simple Rule-Based Chatbot
# Description: A friendly chatbot that responds to general questions
# ------------------------------------------------------------

import datetime
import random

def simple_chatbot():
    print("🤖 Chatbot: Hi! I'm your friendly AI assistant. Type 'bye' to end the chat.\n")


    jokes = [
        "Why did the computer show up at work late? It had a hard drive!",
        "I told my computer I needed a break, and it said 'No problem — I'll go to sleep!'",
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ]

    while True:
        user_input = input("You: ").lower().strip()

       
        if "hello" in user_input or "hi" in user_input:
            print("🤖 Chatbot: Hello there! How's your day going?")
        
       
        elif "your name" in user_input:
            print("🤖 Chatbot: You can call me Chatty — your AI friend!")
        
       
        elif "how are you" in user_input:
            print("🤖 Chatbot: I'm doing great, thanks for asking! What about you?")
        
       
        elif "time" in user_input:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            print(f"🕒 Chatbot: The current time is {current_time}.")
        
        
        elif "date" in user_input:
            current_date = datetime.date.today().strftime("%B %d, %Y")
            print(f"📅 Chatbot: Today's date is {current_date}.")
        
        
        elif "joke" in user_input:
            print("😂 Chatbot:", random.choice(jokes))
       
        elif "thank" in user_input:
            print("🤖 Chatbot: You're most welcome! 😊")
        
    
        elif "bye" in user_input or "exit" in user_input:
            print("🤖 Chatbot: Goodbye! Take care and have a great day! 👋")
            break
        
       
        else:
            print("🤖 Chatbot: Hmm… I'm not sure how to respond to that. Try asking something else!")


if __name__ == "__main__":
    simple_chatbot()
