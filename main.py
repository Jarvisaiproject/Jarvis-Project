# main.py - Entry point for Jarvis

from config import JARVIS_NAME
from core.engine import JarvisEngine

def main():
    print(f"👋 Hello, I’m {JARVIS_NAME}, your AI assistant.")
    
    jarvis = JarvisEngine()
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Jarvis: Goodbye! 👋")
            break
        
        response = jarvis.process_command(user_input)
        print(f"Jarvis: {response}")

if __name__ == "__main__":
    main()
