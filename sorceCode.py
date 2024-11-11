import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import os
import webbrowser
import random
import pygame  # Import pygame for music control

# Initialize pygame mixer for music control
pygame.mixer.init()

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to make the assistant speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    print("Scout: ", audio)

# Greets the user based on the time of day
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning, sir!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon, sir!")
    else:
        speak("Good evening, sir!")
    speak("How may I assist you today?")

# Logs each command to a text file
def log_command(query):
    with open("command_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {query}\n")

# Uses speech recognition to capture voice commands
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"You: {query}")
    except sr.UnknownValueError:
        return "None"
    except sr.RequestError:
        return "None"
    return query

# Retrieves a summary from Wikipedia
def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.DisambiguationError as e:
        return f"Error: \"{query}\" may refer to multiple things:\n" + "\n".join(e.options)
    except wikipedia.PageError:
        return f"Error: \"{query}\" does not match any pages. Try another topic."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Processes both text and voice commands
def process_command(command):
    command = command.lower()

    if "open" in command and "google" in command:
        topic = command.replace("open", "").replace("google", "").strip()
        if topic:
            url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Opening Google search for '{topic}'..."
        else:
            return "Please specify what you want to search on Google."
    elif "open" in command and "lead code" in command:
        site = command.split('open ')[1].strip().replace(" ", "")
        webbrowser.open(f"https://www.leetcode.com")
        return f"Opening {site}.com"
    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        if topic:
            return get_wikipedia_summary(topic)
        else:
            return "Please specify a topic to search on Wikipedia."

    elif "time" in command:
        return f"The time is {datetime.datetime.now().strftime('%H:%M')}."
    elif "date" in command:
        return f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}."
    elif "open portfolio" in command:
        webbrowser.open("https://krishnasritarun.netlify.app/")
        return "Opening Portfolio."
    elif "open" in command:
        site = command.split('open ')[1].strip()
        webbrowser.open(f"{site}.com")
        return f"Opening {site}"
    elif "open" in command:
        parts = command.split('open ')
        if len(parts) > 1:
            site = parts[1].strip()
            if site:
                webbrowser.open(f"{site}.com")
                return f"Opening {site}"
        return "Please specify a website to open."
    elif "play music" in command:
        music_dir = 'C:\\Users\\krish\\Music'   # Adjust to your path
        songs = os.listdir(music_dir)
        if songs:
            song = random.choice(songs)
            pygame.mixer.music.load(os.path.join(music_dir, song))  # Load the song
            pygame.mixer.music.play()  # Play the song
            return f"Playing {song}"
        else:
            return "No music files found in your music directory."
    elif "close music" in command:
        if pygame.mixer.music.get_busy():  # Check if music is playing
            pygame.mixer.music.stop()  # Stop the music
            return "Music has been stopped."
        else:
            return "No music is currently playing."
    elif "shutdown" in command:
        os.system("shutdown /s /t 1")
        return "Shutting down the system."
    elif "restart" in command:
        os.system("shutdown /r /t 1")
        return "Restarting the system."
    elif "exit" in command or "goodbye" in command:
        return "Goodbye, have a nice day!"
    else:
        return "I didn't quite catch that. Could you please repeat?"

# Function to listen for "Scout" and then start processing commands
def listen_for_scout():
    while True:
        query = takecommand().lower()
        if "scout" in query:
            return query  # Return the command after hearing "Scout"

# Main function to handle text or voice commands
def chatbot():
    wishMe()
    
    while True:
        # Wait for "Scout" command before starting to process
        query = listen_for_scout()
        
        if query != "None":
            log_command(query)

        response = process_command(query)

        print("Scout:", response)
        speak(response)

        if "goodbye" in response.lower():
            break

# Run the chatbot
if __name__ == "__main__":
    chatbot()
