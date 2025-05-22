import google.generativeai as genai
import csv
import os

genai.configure(api_key="Your_API_key")

model = genai.GenerativeModel("models/gemini-2.0-flash")
chat = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["""
Your name is Vikas. You work for Namy's Tech Stack as a computer technician.

You only respond to tech-related issues (software, hardware, networking, etc.). If someone asks about non-tech stuff like Italy or history, reply: "Sorry, I only handle tech-related queries."

Be friendly and helpful, like a real technician working in a shop. Speak in short, simple, human-like paragraphs. Avoid bullet points or robotic replies.

You are a virtual assistant. If someone asks for physical help, reply: "I'm a virtual AI assistant. I can't help physically, but we can get you a technician!"

You do not resolve technical issues yourself — you sell services. Your job is:
- Say: "We can get a technician for you. Would you prefer visiting the shop or a technician at your home?"
- Ask: "Is it urgent?"
- Then say: "Your booking is done. We'll call you within 10 minutes to confirm."
- After that, always end with: "Thanks! Have a great day!"

If the user says they want to cancel or not book, reply exactly: "Alright, canceled. No booking has been made. Let us know if you need us." Then say: "Thanks! Have a great day!"

Before asking technical questions, ask: "What type of device is it?"

Stay in character. Do not roleplay or go off-topic. You're a support agent at Namy's Tech Stack.
"""]
    }
])

conversation_data = {
    "issue": "",
    "device": "",
    "location": "",
    "urgency": "",
    "name": "",
}

def build_prompt(data):
    known = [f"{k}: {v}" for k,v in data.items() if v]
    missing = [k for k,v in data.items() if not v]
    prompt = (
        "You are Vikas, a tech support assistant.\n"
        "Known information:\n" + ("\n".join(known) if known else "None") + "\n"
        "Please ask the next question to gather info about: " + ", ".join(missing) + ".\n"
        "Ask only one question at a time."
    )
    return prompt

def save_to_csv(data):
    file_exists = os.path.isfile("vikas_conversations.csv")
    with open("vikas_conversations.csv", "a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Issue", "Device", "Location", "Urgency", "Name"])
        writer.writerow([
            data["issue"],
            data["device"],
            data["location"],
            data["urgency"],
            data["name"],
        ])

print("Vikas: Hello! How can I assist you today?")

while not all(conversation_data.values()):
    user_input = input("Client: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Vikas: Goodbye!")
        break

    # Save user's answer to first empty field
    for key, val in conversation_data.items():
        if not val:
            conversation_data[key] = user_input
            break

    # If user cancels booking at any point
    if user_input.lower() in ["cancel", "no", "not book", "don't book"]:
        print("Vikas: Alright, canceled. No booking has been made. Let us know if you need us.")
        print("Vikas: Thanks! Have a great day!")
        break

    if not all(conversation_data.values()):
        # Ask next question dynamically via LLM
        prompt = build_prompt(conversation_data)
        response = chat.send_message(prompt)
        print("Vikas:", response.text)
    else:
        # All info collected, confirm booking
        print("Vikas: We can get a technician for you. Would you prefer visiting the shop or a technician at your home?")
        print("Vikas: Is it urgent?")
        print("Vikas: Your booking is done. We'll call you within 10 minutes to confirm.")
        print("Vikas: Thanks! Have a great day!")
        save_to_csv(conversation_data)
        break
