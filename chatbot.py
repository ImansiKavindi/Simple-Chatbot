import random
import tkinter as tk
from tkinter import Canvas, Entry, Button, Scrollbar, Frame
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pyttsx3
import time
import threading

# Initialize TTS Engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Define Bot Responses
responses = {
     "sad": [
        "It's okay to feel sad sometimes. The sun will shine again.",
        "Tough times don’t last, but tough people do.",
        "You are allowed to feel not okay, but don't let it define you.",
        "Feeling sad is a natural part of life's ebb and flow. You're not alone.",
       "In the midst of sadness, remember, tomorrow is a new day filled with possibilities.",
       "Your strength is greater than any sadness you may feel. Keep pushing forward.",
       "Allow yourself to feel sad today, knowing that brighter days are ahead.",
        "Healing takes time, but you're getting closer to peace."
    ],
    "failure": [
        "Failure is simply the opportunity to begin again.",
        "Don’t be afraid to fail. Be afraid of not trying.",
        "Every setback is a setup for a comeback.",
        "Failure is a stepping stone towards success. Keep moving forward.",
        "Every failure brings a lesson that prepares you for the next challenge.",
         "Your resilience in the face of failure is a testament to your growth.",
        "Don't let failure define your journey; let it refine your path to greatness.",
        "Your mistakes don’t define you; they refine you."
    ],
    "love": [
        "Love is not about perfection, it's about growth.",
        "True love is built on trust and patience.",
        "Sometimes the right person comes at the wrong time.",
        "Love is a journey of discovery, both of others and of yourself.",
        "Cherish the love you have today, for it shapes the memories of tomorrow.",
        "Love grows through understanding, compassion, and shared experiences.",
        "The beauty of love lies in its ability to inspire and uplift us in unexpected ways.",
        "Love yourself first, and everything else falls into place."
    ],
    "default": [
        "I'm here to help. Can you tell me more about how you're feeling?",
        "I'm listening. Please share your thoughts with me.",
        "It's okay to open up. What's on your mind?",
        "You're stronger than you know. Take your time, and let me know how I can support you.",
        "It's okay to feel what you're feeling. I'm here to listen whenever you're ready.",
        "You're not alone in this. Reach out whenever you need a listening ear.",
        "Remember, every challenge is a chance for growth. You're on a path to brighter days.",
        "I'm here for you. Feel free to express yourself."
    ]
}

# Emotion Keywords
sad_keywords = ['sad', 'unhappy', 'depressed', 'down']
fail_keywords = ['failed', 'frustrated', 'losing', 'disappointed']
love_keywords = ['love', 'relationship', 'heartbroken','didnt love']

# Function to Detect Emotion and Provide Response
def detect_emotion(user_input):
    score = analyzer.polarity_scores(user_input)
    if score['compound'] <= -0.05:
        return random.choice(responses["sad"])
    elif any(word in user_input.lower() for word in fail_keywords):
        return random.choice(responses["failure"])
    elif any(word in user_input.lower() for word in love_keywords):
        return random.choice(responses["love"])
    else:
        return random.choice(responses["default"])

# Function to Create Message Bubbles
def create_message_bubble(text, user=True):
    bubble_frame = Frame(chat_frame, bg="#25D366" if user else "#E5E5EA")
    msg_label = tk.Label(
        bubble_frame, text=text, wraplength=350, font=("Arial", 12),
        bg="#25D366" if user else "#E5E5EA", fg="white" if user else "black",
        padx=10, pady=5, relief=tk.FLAT, bd=0
    )
    msg_label.pack()

    if user:
        bubble_frame.pack(anchor='e', padx=10, pady=5)
    else:
        bubble_frame.pack(anchor='w', padx=10, pady=5)

    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)

# Function to Handle User Input
def handle_input():
    user_message = user_input.get().strip()
    if not user_message:
        return

    create_message_bubble(user_message, user=True)
    user_input.delete(0, tk.END)
    root.update()

    time.sleep(0.5)
    response = detect_emotion(user_message)
    create_message_bubble(response, user=False)
    speak_response(response)

# Function to Speak Response in a Separate Thread
def speak_response(text):
    threading.Thread(target=lambda: engine.say(text) or engine.runAndWait(), daemon=True).start()

# Initialize GUI
root = tk.Tk()
root.title("ChatBot UI")
root.geometry("400x600")
root.resizable(False, False)
root.configure(bg="white")

# Chat Canvas
chat_canvas = Canvas(root, bg="white", highlightthickness=0)
chat_scrollbar = Scrollbar(root, command=chat_canvas.yview)
chat_frame = Frame(chat_canvas, bg="white")
chat_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))
chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")
chat_canvas.configure(yscrollcommand=chat_scrollbar.set)

chat_canvas.pack(side="top", fill="both", expand=True, padx=10, pady=10)
chat_scrollbar.pack(side="right", fill="y")

# Input Field
user_input = Entry(root, font=("Arial", 14), bg="#F0F0F0", fg="black", relief=tk.FLAT)
user_input.pack(side="left", fill="x", padx=10, pady=10, expand=True)

# Send Button
send_button = Button(root, text="Send", font=("Arial", 12, "bold"), bg="#25D366", fg="white", command=handle_input)
send_button.pack(side="right", padx=10, pady=10)

# Initial Bot Message
create_message_bubble("Hello! How are you feeling today?", user=False)

# Bind Enter Key
def enter_pressed(event):
    handle_input()

user_input.bind("<Return>", enter_pressed)

# Run GUI
root.mainloop()
