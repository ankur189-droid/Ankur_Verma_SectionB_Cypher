import streamlit as st
import threading
import time
import speech_recognition as sr
from back import wishMe, speak, process_command as backend_process_command
import webbrowser
import os
import subprocess
from pathlib import Path

# Load Custom CSS
def load_custom_css():
    st.markdown("""
        <style>
        /* Base Styles */
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
            color: #e0e0e0;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            background-attachment: fixed;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Futuristic Background Animation */
        .particle-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: url('https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2Q1N2M2YzZiNjU0YzVhNzVhYzZiNzZiYzZiNzZiYzZiNzZiYzZiN2I2&rid=giphy.gif') center/cover no-repeat;
            opacity: 0.2;
            pointer-events: none;
            animation: backgroundPulse 20s ease-in-out infinite;
        }
        
        @keyframes backgroundPulse {
            0% { opacity: 0.2; transform: scale(1); }
            50% { opacity: 0.25; transform: scale(1.02); }
            100% { opacity: 0.2; transform: scale(1); }
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Orbitron', sans-serif;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            letter-spacing: 1px;
        }
        
        h1 {
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
        }
        
        h3 {
            font-size: 1.5rem;
            margin-top: 0;
        }
        
        /* Buttons */
        .stButton>button {
            border: none;
            border-radius: 50px;
            background: linear-gradient(45deg, #4776E6, #8E54E9);
            color: white;
            font-weight: bold;
            padding: 0.75rem 1.5rem;
            box-shadow: 0 4px 15px rgba(71, 118, 230, 0.4);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            z-index: 1;
        }
        
        .stButton>button:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #8E54E9, #4776E6);
            z-index: -1;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(71, 118, 230, 0.6);
        }
        
        .stButton>button:hover:before {
            opacity: 1;
        }
        
        .stButton>button:active {
            transform: translateY(1px);
        }
        
        /* Mic Button */
        .mic-button {
            background: linear-gradient(45deg, #00d2ff, #3a7bd5);
            border-radius: 50%;
            width: 120px;
            height: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px auto;
            box-shadow: 0 0 25px rgba(0, 210, 255, 0.6);
            transition: all 0.3s ease;
            cursor: pointer;
            animation: pulse 2s infinite;
        }
        
        .mic-button:hover {
            transform: scale(1.1);
            box-shadow: 0 0 35px rgba(0, 210, 255, 0.8);
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 210, 255, 0.7); }
            70% { box-shadow: 0 0 0 15px rgba(0, 210, 255, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 210, 255, 0); }
        }
        
        /* Log Card - Glass Morphism */
        .log-card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            padding: 1.5rem;
            margin-top: 2rem;
            transition: all 0.3s ease;
        }
        
        .log-card:hover {
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.5);
        }
        
        /* Floating Animation */
        .floating {
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
            100% { transform: translateY(0px); }
        }
        
        /* Status Messages */
        .stAlert {
            border-radius: 12px;
            border-left: 5px solid;
        }
        
        .stSuccess {
            border-color: #00d2ff;
            background: rgba(0, 210, 255, 0.1);
        }
        
        .stError {
            border-color: #ff4d4d;
            background: rgba(255, 77, 77, 0.1);
        }
        
        .stWarning {
            border-color: #ffcc00;
            background: rgba(255, 204, 0, 0.1);
        }
        
        /* Checkbox Styling */
        .stCheckbox>label {
            color: #e0e0e0;
            font-weight: 500;
        }
        
        .stCheckbox>div>div {
            background: linear-gradient(45deg, #4776E6, #8E54E9);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            h1 {
                font-size: 2rem;
            }
            
            .mic-button {
                width: 100px;
                height: 100px;
            }
        }
        
        /* Font Import */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Roboto:wght@400;500&display=swap');
        </style>
    """, unsafe_allow_html=True)

# Streamlit page setup
st.set_page_config(page_title="Cypher — Voice Assistant", page_icon="🤖", layout="centered")
load_custom_css()

# Particle background
st.markdown('<div class="particle-background"></div>', unsafe_allow_html=True)

# Fancy loading screen
if 'loaded' not in st.session_state:
    with st.spinner('Booting Cypher Systems...'):
        time.sleep(3)
    st.session_state.loaded = True

# Title and tagline
st.markdown("<h1>Cypher — Your Personal AI Voice Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Command the Future.</h3>", unsafe_allow_html=True)

# Initialize session state
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'started' not in st.session_state:
    st.session_state.started = False
if 'continuous' not in st.session_state:
    st.session_state.continuous = False

# Function to recognize voice from mic
def recognize_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Recording... Please Speak Now")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            st.warning("No speech detected within timeout period")
            return "None"
    
    try:
        st.success("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        st.session_state.logs.append(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand. Please try again.")
        return "None"
    except Exception as e:
        st.error(f"Recognition error: {str(e)}")
        return "None"

# Wrapper function to process commands
def process_command(query):
    try:
        response = backend_process_command(query)
        if response:
            st.session_state.logs.append(f"System: {response}")
            st.success(response)
    except Exception as e:
        error_msg = f"Error processing command: {str(e)}"
        st.session_state.logs.append(error_msg)
        st.error(error_msg)
        speak("Sorry, I encountered an error processing that command")

# Main control buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('🎤 Start Cypher'):
        wishMe()
        st.session_state.started = True
        st.session_state.logs.append("System: Cypher activated")

with col2:
    if st.button('🛑 Stop Cypher'):
        st.session_state.started = False
        st.session_state.continuous = False
        st.session_state.logs.append("System: Cypher deactivated")
        st.success("Assistant Stopped.")

with col3:
    if st.session_state.started:
        st.session_state.continuous = st.checkbox('Continuous Listening', value=st.session_state.continuous)

# Command interface
if st.session_state.started:
    st.markdown('<div class="mic-button floating">🎤</div>', unsafe_allow_html=True)
    
    if st.button('🎙️ Record Command') or st.session_state.continuous:
        command = recognize_from_mic()
        if command != "None":
            process_command(command)
            if st.session_state.continuous:
                time.sleep(1)  # Small delay between continuous listens
                st.experimental_rerun()

# Logs display
st.markdown('<div class="log-card">', unsafe_allow_html=True)
st.subheader("Activity Logs")
for log in st.session_state.logs[-10:]:  # Show last 10 logs
    st.write(log)
st.markdown('</div>', unsafe_allow_html=True)