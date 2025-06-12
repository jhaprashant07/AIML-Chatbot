import aiml
import os
import tkinter as tk
from tkinter import scrolledtext

# Set up AIML kernel
kernel = aiml.Kernel()
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="startup.xml", commands="LOAD AIML B")
    kernel.saveBrain("bot_brain.brn")

# Define GUI
class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AIML Chatbot")
        self.root.geometry("500x500")

        # Chat window
        self.chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # User input field
        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if user_input == "":
            return

        self.append_to_chat("You: " + user_input)
        self.entry.delete(0, tk.END)

        if user_input.lower() == "exit":
            self.append_to_chat("Bot: Bye!")
            self.root.quit()
            return

        bot_response = kernel.respond(user_input)
        self.append_to_chat("Bot: " + bot_response)

    def append_to_chat(self, message):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
