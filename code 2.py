# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 20:40:45 2024

@author: Nandana S
"""

import cv2
from deepface import DeepFace
import pyttsx3
from flask import Flask, render_template, request

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Flask app for interaction
app = Flask(__name__)

# Function to detect emotion
def detect_emotion(frame):
    try:
        # Analyze emotion using DeepFace
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result['dominant_emotion']
        return dominant_emotion
    except Exception as e:
        print(f"Error detecting emotion: {e}")
        return "neutral"

# Function to respond to emotion
def respond_to_emotion(emotion):
    responses = {
        "happy": "You look happy today! Keep smiling!",
        "sad": "I see you're feeling sad. Would you like to hear a joke?",
        "angry": "Take a deep breath. It's okay to feel angry sometimes.",
        "neutral": "Hello! How can I help you today?",
    }
    response = responses.get(emotion, "I'm here for you no matter how you're feeling.")
    engine.say(response)
    engine.runAndWait()
    return response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/emotion", methods=["POST"])
def emotion():
    # Capture frame from webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return "Could not access the webcam."
    
    # Detect emotion
    emotion = detect_emotion(frame)
    # Respond to the emotion
    response = respond_to_emotion(emotion)
    return {"emotion": emotion, "response": response}

if __name__ == "__main__":
    app.run(debug=True)
