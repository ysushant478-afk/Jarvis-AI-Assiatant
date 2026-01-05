import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import pywhatkit
import wikipedia
import os
import sys

# Voice Settings
engine = pyttsx3.init()
engine.setProperty("rate", 180) 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_command():
    r = sr.Recognizer()
    r.pause_threshold = 1.0
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User: {query}")
            return query.lower()
        except Exception:
            return ""

def main():
    speak("Hello boss, I am online. How can I help you?")

    while True:
        query = listen_command()
        
        if query == "":
            continue

        # --- 1. EXIT (Sabse upar rakha hai taaki instant response mile) ---
        if any(word in query for word in ["exit", "stop", "bye", "quit", "offline"]):
            speak("Goodbye boss! Now systems are offline.")
            # sys.exit() direct program ko kill kar dega
            sys.exit() 

        # --- 2. GENERAL GREETINGS ---
        elif any(word in query for word in ["hello", "hi", "hey"]):
            speak("Hello boss! How can I assist you today?")

        elif "how are you" in query or "how r u" in query:
            speak("I am doing great boss! Thank you for asking.")

        elif "what is your name" in query:
            speak("I am Jarvis, your personal AI assistant.")

        # --- 3. TIME ---
        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")    
            speak(f"Boss, the time is {strTime}")
    
        # --- DATE FEATURE ---
        elif "date" in query or "day" in query:
            # Aaj ki date extract karna
            today = datetime.datetime.now()
            # Format: Day, Month Date, Year (e.g., Friday, December 26, 2025)
            full_date = today.strftime("%A, %B %d, %Y")
            speak(f"Boss, today is {full_date}")

        # --- TIMES OF INDIA NEWS COMMAND ---
        elif "news" in query:
            speak("Opening Times of India headlines for you, boss.")
            webbrowser.open("https://timesofindia.indiatimes.com/home/headlines")

        # --- 4. YOUTUBE PLAY ---
        elif "play" in query:
            song_name = query.replace("play", "").strip()
            speak(f"Playing {song_name} on YouTube")
            pywhatkit.playonyt(song_name)

        # --- WEATHER & TEMPERATURE FEATURE ---
        elif "weather" in query or "temperature" in query:
            speak("Which city's weather should I check?")
            city = listen_command()
            if city:
                speak(f"Fetching weather information for {city}...")
                # Google search for live weather
                webbrowser.open(f"https://www.google.com/search?q=weather+in+{city}")
                speak(f"Here is the current temperature and weather for {city} on your screen.")
            else:
                speak("I didn't catch the city name. Please try again.")

        # --- WIKIPEDIA FEATURE ---
        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            # 'wikipedia' word ko query se hata dete hain taaki sirf topic bache
            query = query.replace("wikipedia", "").strip()
            try:
                # Sirf 2 sentences ki summary nikalega
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia...")
                speak(results)
            except Exception as e:
                speak("Sorry boss, I couldn't find any information on Wikipedia about that.")

        # --- LOCATION FEATURE ---
        elif "where is" in query or "location of" in query:
            # Query se 'where is' hata kar sirf jagah ka naam nikalna
            place = query.replace("where is", "").replace("location of", "").strip()
            if place:
                speak(f"Locating {place} on Google Maps, boss.")
                webbrowser.open(f"https://www.google.com/maps/search/{place}")
            else:
                speak("Which place do you want to find, boss?")

        # --- 5. GOOGLE SEARCH ---
        elif "google" in query:
            speak("What should I search for?")
            search_data = listen_command()
            if search_data:
                webbrowser.open(f"https://www.google.com/search?q={search_data}")
                speak(f"Searching for {search_data}")

        # --- 6. DYNAMIC APPLICATION OPENER ---
        elif "open" in query:       
            app_name = query.replace("open", "").strip()
            speak(f"Opening {app_name}")
            
            apps = {
                "word": "winword",
                "excel": "excel",
                "chrome": "chrome",
                "notepad": "notepad",
                "calculator": "calc"
            }

            if app_name in apps:
                os.system(f"start {apps[app_name]}")
            else:
                try:
                    os.system(f"start {app_name}")
                except Exception:
                    speak(f"I couldn't find {app_name}.")

        # --- 7. FALLBACK ---
        else:
            print("Command not matched in database.")

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        # Jab sys.exit() call hota hai toh ye handle karta hai
        pass
    except KeyboardInterrupt:
        print("\nForcefully stopped.")
        sys.exit()