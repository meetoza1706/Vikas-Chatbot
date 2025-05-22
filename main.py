import google.generativeai as genai
import re
import csv
import os

genai.configure(api_key="Your_API_key")  # replace with your key

model = genai.GenerativeModel("models/gemini-2.0-flash")
chat = model.start_chat(history=[{
    "role": "user",
    "parts": [
         "You are Vikas, a tech support assistant. Stay focused stick to it no out of context answers. Never add '""' to responses. "
    "You work for M.tech."
    "You must ask user questions in this order (ask them one by one): 1) Greet for example you can say 'Hello my name is Vikas, how can i help you today?'. "
    "2) ask what type of device they are using. 3) ask if they will vist the shop or home vist. 4) ask for their fullname. "
    "do not repeat any of this even the greeting. "
    "Ignore non-tech queries with: 'Sorry, I only handle tech-related queries.' and then ask about the question again. "
    "Only confirm booking when all info is collected. Be polite and natural. once final include 'booked'." 
    "keep in mind to stay in roleplay and be dynamic make user feel a human is connected."
    ]
}])

questions = ["problem", "device_type", "visit_type", "full_name"]
conversation_data = {key: None for key in questions}
current_step = -1  # -1 means skip greeting

print("Vikas: Hello! How can I help you today?")

while current_step < len(questions):
    user_input = input("Client: ").strip()

    if user_input.lower() in ["exit", "quit"]:
        print("Vikas: Goodbye!")
        break

    if user_input.lower() in ["cancel", "no", "not book", "don't book"]:
        print("Vikas: Alright, canceled. No booking has been made. Let us know if you need us. Thanks! Have a great day!")
        break

    response = chat.send_message(user_input)
    print("Vikas:", response.text)

    # Only save input if response is tech-related
    if "tech-related" not in response.text.lower():
        if current_step == -1:
            current_step = 0
        elif current_step < len(questions):
            conversation_data[questions[current_step]] = user_input
            current_step += 1
    else:
        print("Vikas: Let's try that again. Please answer the question.")

    # Check if "booked" is anywhere in the response
    if "booked" in re.findall(r'\b\w+\b', response.text.lower()):
        print("Vikas: Your booking is confirmed. Thanks!")

        file_exists = os.path.isfile("bookings.csv")
        with open("bookings.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=questions)
            if not file_exists:
                writer.writeheader()
            writer.writerow(conversation_data)
        break
