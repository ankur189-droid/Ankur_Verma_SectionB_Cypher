import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import pyautogui
import time
import threading
import subprocess
from pathlib import Path
import sys
import json

# Configuration
CONFIG_FILE = "cypher_config.json"
DEFAULT_CONFIG = {
    "whatsapp_path": "",
    "whatsapp_web": "https://web.whatsapp.com",
    "screenshot_dir": "screenshots",
    "passkey": "ankur"
}

# Load or create config
def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
    except Exception:
        pass
    return DEFAULT_CONFIG

config = load_config()

# Initialize the speech engine
try:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 185)
except Exception as e:
    print(f"Error initializing TTS engine: {e}")
    engine = None

# Function to speak text
def speak(text):
    if not engine:
        print(f"[TTS]: {text}")
        return
        
    def speak_thread():
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in speech: {e}")

    threading.Thread(target=speak_thread, daemon=True).start()

# Wishing as per time of the day   
def wishMe():
    hour = int(time.strftime("%H"))
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 17:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

# Enhanced voice recognition
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("No speech detected")
            return "None"
    
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "None"
    except Exception as e:
        print(f"Recognition error: {e}")
        return "None"

# Command processing - now returns response messages
def process_command(query):
    if query == "None":
        return "Didn't catch that, please try again"

    query = query.lower()
    response = None

    try:
        # Authentication commands
        if 'hello cypher' in query:
            speak("Yes sir. Please tell me your passkey.")
            passkey = listen().lower()
            if config['passkey'] in passkey:
                speak("Access granted.")
                response = "Access granted"
            else:
                speak("Access denied.")
                response = "Access denied"
        
        # Information commands
        elif 'who are you' in query:
            response = "I am Cypher, your virtual assistant"
            speak(response)
        
        elif 'who created you' in query:
            response = "I was created by Ankur Verma using Python"
            speak(response)
        
        # Browser commands
        elif 'open google' in query:
            webbrowser.open('https://google.com')
            response = "Opened Google"
            speak(response)
        
        elif 'search on google' in query:
            webbrowser.open('https://google.com')
            time.sleep(1)
            speak('What should I search?')
            search_term = listen().lower()
            if search_term != "None":
                pyautogui.typewrite(search_term, 0.1)
                pyautogui.press('enter')
                response = f"Searching Google for {search_term}"
            else:
                response = "Google search cancelled"
            speak(response)
        
        # System commands
        elif 'open command prompt' in query:
            subprocess.Popen('cmd', shell=True)
            response = "Command Prompt opened"
            speak(response)
        
        elif 'close command prompt' in query:
            os.system("taskkill /f /im cmd.exe")
            response = "Command Prompt closed"
            speak(response)
        
        # WhatsApp commands
        elif 'open whatsapp' in query:
            if config['whatsapp_path'] and os.path.exists(config['whatsapp_path']):
                os.startfile(config['whatsapp_path'])
                response = "Opening WhatsApp application"
            else:
                webbrowser.open(config['whatsapp_web'])
                response = "Opening WhatsApp Web"
            speak(response)
            time.sleep(2)
        
        # Screenshot functionality
        elif 'take screenshot' in query:
            screenshot_dir = Path(config['screenshot_dir'])
            screenshot_dir.mkdir(exist_ok=True)
            
            speak('Tell me a name for the file')
            name = listen().lower()
            if name == "None":
                name = f"screenshot_{int(time.time())}"
            
            img = pyautogui.screenshot()
            save_path = screenshot_dir / f"{name}.png"
            img.save(save_path)
            response = f"Screenshot saved as {save_path}"
            speak("Screenshot saved")
        
        # System control
        elif 'go to sleep' in query or 'exit' in query:
            response = "Goodbye, shutting down"
            speak(response)
            return "shutdown"
        
        # Default response
        else:
            response = f"Executed: {query}"
            speak(f"You said: {query}")

    except Exception as e:
        response = f"Error processing command: {str(e)}"
        print(response)
        speak("Sorry, I encountered an error")

    return response

# Main function for standalone operation
if __name__ == "__main__":
    wishMe()
    while True:
        query = listen().lower()
        if query == "None":
            continue
            
        result = process_command(query)
        if result == "shutdown":
            break