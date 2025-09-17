import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import sys
import datetime

# Set your Google Gemini API Key here
GOOGLE_API_KEY = "AIzaSyA0d4ENwzb7wR93ultlqywft3pK8naPdhw"

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
try:
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
except Exception as e:
    print("Error initializing Gemini model:", e)

    sys.exit(1)

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Recognize voice input from user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return "Listening timed out."
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "Network error."

def get_real_world_time():
    """Get real-world date and time."""
    now = datetime.datetime.now()
    formatted_time = now.strftime("%A, %B %d, %Y, %I:%M %p")  # Example: Monday, March 25, 2025, 02:30 PM
    return f"Today's date and time is {formatted_time}."

def get_gemini_response(prompt):
    """Fetch response from Google Gemini API."""
    try:
        response = model.generate_content([prompt])  # Pass prompt as a list (as required in the latest SDK)
        return response.text
    except Exception as e:
        print("Error details:", e)
        return "Error fetching response from Gemini AI."

def main():
    speak("Hello! How can I help you?")
   
    try:
        while True:
            command = listen()

            if "exit" in command or "stop" in command:
                speak("Goodbye! Have a nice day.")
                break

            # Check if user asked for date or time
            elif "time" in command or "date" in command:
                response = get_real_world_time()
            else:
                response = get_gemini_response(command)

            print("Assistant:", response)
            speak(response)
    except KeyboardInterrupt:
        speak("Goodbye! Have a nice day.")
        sys.exit(0)

if __name__ == "__main__":
    main()
