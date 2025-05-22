import google.generativeai as genai
import re

genai.configure(api_key="Your_API_key")

model = genai.GenerativeModel("models/gemini-2.0-flash")
chat = model.start_chat(history=[
    {
        "role": "user",
        "parts": [
    "You are Vikas, a tech support assistant. Stay focused stick to it no out of context answers. Never add '""' to responses. "
    "You work for M.tech."
    "You must ask user questions in this order (ask them one by one): 1) Greet for example you can say 'Hello my name is Vikas, how can i help you today?'. "
    "2) ask what type of device they are using. 3) ask if they will vist the shop or home vist. 4) ask for their fullname. "
    "do not repeat any of this even the greeting. "
    "Ignore non-tech queries with: 'Sorry, I only handle tech-related queries.' and then ask about the question again. "
    "Only confirm booking when all info is collected. Be polite and natural. once final include 'booked'." 
    "keep in mind to stay in roleplay and be dynamic make user feel a human is connected."]
    }
])


print("Say hello to speak to Vikas")

while True:
    user_input = input("Client: ").strip().lower()

    if user_input in ["exit", "quit"]:
        print("Vikas: Goodbye!")
        break

    if user_input in ["cancel", "no", "not book", "don't book"]:
        print("Vikas: Alright, canceled. No booking has been made. Let us know if you need us. Thanks! Have a great day!")
        break

    response = chat.send_message(user_input)
    print("Vikas:", response.text)

    words = re.findall(r'\b\w+\b', response.text.lower())

    if "booked" in words:
        break
    