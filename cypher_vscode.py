import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import pyautogui
import time

# Initializing the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[0].id) 
engine.setProperty('rate', 185) 

# Function to speak text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
 
#Wishing as per time of the day   
def wishMe(): 
    hour = int(datetime.datetime.now().hour) 
    if hour>=0 and hour<12: 
        speak("Good Morning!") 
    elif hour>=12 and hour<18: 
        speak("Good Afternoon!")    
    else: 
        speak("Good Evening!") 
    speak("What can I do for you ?")

# Function to listen for speech and return text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.9
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query
    except Exception as e:     
        print("Say that again please...")   
        return "None"

# Main function to run the chatbot with voice
if __name__ == "__main__":
    wishMe()
    while True:
        query = listen().lower()
        if 'hello cypher' in query:
            print("yes sir")
            speak("yes sir")
            print('how may i help you, but before that Tell me your passkey')
            speak('how may i help you, but before that tell me your passkey')
            name = listen().lower()
            if 'ankur' in name:
                print('access granted')
                speak('access granted')
            else:
                print('Access denied')
                speak('access denied')
                time.sleep(0.5)
                pyautogui.click(x=1052, y=53, clicks=1, interval=0, button="left")
        
        elif 'who are you' in query:
            print('my name is cypher')
            speak('my name is cypher')
            print('i am your virtual assistant')
            speak('i am your virtual assistant')
            
        elif 'what can you do' in query:
            print('i can do everything that my creator programmed me to do')
            speak('i can do everything that my creator programmed me to do')
            
        elif 'who created you' in query:
            print('i am created by Ankur Verma using VS code')
            speak('i am created by Ankur Verma using VS code')
            
        elif 'open google' in query:
            webbrowser.open('google.com')
            
        
        elif 'search on google' in query:
            webbrowser.open('google.com')
            time.sleep(1.4)
            speak('what should i search')
            qy = listen().lower()
            pyautogui.typewrite(qy, 0.2)
            pyautogui.press('enter')
            
        elif 'open incognito' in query:
            pyautogui.hotkey('ctrl', 'shift', 'n')
            
        elif 'open history' in query: 
            pyautogui.hotkey('ctrl', 'h')
            
        elif 'open downloads' in query: 
            pyautogui.hotkey('ctrl', 'j')
            
        elif 'previous tab' in query: 
            pyautogui.hotkey('ctrl', 'shift', 'tab')
            
        elif 'next tab' in query: 
            pyautogui.hotkey('ctrl', 'tab')
            
        elif 'new tab' in query:
            pyautogui.hotkey('ctrl', 't')
            
        elif 'close tab' in query: 
            pyautogui.hotkey('ctrl', 'w')

        elif 'close browser' in query:
             os.system("taskkill /f /im msedge.exe")
             
        elif 'close brave' in query:
             os.system("taskkill /f /im brave.exe")
             
        elif 'close chrome' in query:
             os.system("taskkill /f /im msedge.exe")
             
    
        elif 'open youtube' in query:
            webbrowser.open('youtube.com')
            time.sleep(2)
            speak('what should i search')
            pyautogui.click(x=342, y=99, clicks=1, button='left')
            qyt = listen().lower()
            pyautogui.typewrite(qyt, 0.2)
            pyautogui.press('enter')
            
            
        elif 'search on youtube' in query:
            query = query.replace("search on youtube", "")
            time.sleep(5)
            webbrowser.open(f"www.youtube.com/results?search_query{query}")
            
        elif "restart the system" in query: 
            os.system("shutdown /r /t 5")
            
        elif "Lock the system" in query: 
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            
        elif "open command prompt" in query: 
            os.system("start cmd")
            
        elif "close command prompt" in query: 
            os.system("taskkill /f /im cmd.exe")
            
        elif 'go to sleep' in query:
            print('alright, i am switching off')
            speak('alright, i am switching off')
            time.sleep(1)
            pyautogui.click(x=1052, y=53, clicks=1, interval=0, button="left")
            
        elif "take screenshot" in query: 
            speak('tell me a name for the file') 
            name = listen().lower() 
            time.sleep(3) 
            img = pyautogui.screenshot()   
            img.save(f"{name}.jpg")   
            speak("screenshot saved")
            
            
        elif "volume up" in query: 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup") 
            
        elif "volume down" in query: 
            pyautogui.press("medown") 
            pyautogui.press("volumedown") 
            pyautogui.press("volumedown") 
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            
        elif 'open whatsapp' in query:
            pyautogui.press('win')
            pyautogui.typewrite('whatsapp', 0.2)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(2)
            pasw = listen().lower()
            if 'enter my password' in pasw:
                pyautogui.click(x=19, y=827, clicks=1, interval=0, button='left')
                pyautogui.typewrite('chhinar', 0.2)
                pyautogui.press('enter')
            
        elif 'open group' in query:
            pyautogui.press('win')
            pyautogui.typewrite('whatsapp', 0.2)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(2)
            pyautogui.click(x=19, y=827, clicks=1, interval=0, button='left')
            pyautogui.typewrite('chhinar', 0.2)
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.typewrite('krmu')
            pyautogui.click(x=255, y=182, clicks=1, interval=0, button="left")   
            