import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import datetime
import pyjokes

# --- INITIALIZATION ---
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id) 

def speak(audio):
    """Outputs text to both console and voice."""
    print(f"Gyaani: {audio}")
    engine.say(audio)
    engine.runAndWait()

def get_user_name():
    """Always asks for the user's name at startup."""
    print("--- 🧠 Gyaani System Initializing ---")
    speak("Hello! I am Gyaani. Before we start, may I know your name?")
    # Input is best here for name accuracy
    name = input("Enter your name: ").strip()
    if not name:
        name = "User" # Fallback if empty
    return name

def take_command():
    """Takes input via Voice with a Text fallback."""
    r = sr.Recognizer()
    query = "None"
    
    with sr.Microphone() as source:
        print("\n[Listening... or type below]")
        r.pause_threshold = 0.8
        try:
            # Listens for a few seconds
            audio = r.listen(source, timeout=4, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You (Voice): {query}")
        except Exception:
            print("Keyboard Input Mode Active:")
            query = input("You (Type): ")
    
    return query.lower()

def wish_me(name):
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        greet = "Good Morning"
    elif hour < 18:
        greet = "Good Afternoon"
    else:
        greet = "Good Evening"
    speak(f"{greet} {name}. Gyaani is now at your service.")

if __name__ == '__main__':
    # Step 1: Always ask for name first
    user_name = get_user_name()
    
    # Step 2: Greet the user
    wish_me(user_name)
    
    while True:
        query = take_command()

        if query == "none" or query == "":
            continue

        # Commands
        if 'exit' in query or 'sleep' in query or 'stop' in query:
            speak(f"Goodbye {user_name}! Systems powering down.")
            break

        elif 'open google' in query:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        elif 'search on google' in query or 'google search' in query:
            speak("What should I search for?")
            search_content = take_command()
            if search_content != "none":
                speak(f"Searching Google for {search_content}")
                webbrowser.open(f"https://www.google.com/search?q={search_content}")

        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(query, sentences=2)
                speak(results)
            except:
                speak("I couldn't find that topic.")

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {strTime}")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            speak("Opening YouTube.")

        else:
            speak(f"Should I search Google for '{query}'?")
            ans = take_command()
            if 'yes' in ans or 'sure' in ans:
                webbrowser.open(f"https://www.google.com/search?q={query}")