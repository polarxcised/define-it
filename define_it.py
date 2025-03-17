import requests
import pyfiglet
import difflib
import pyttsx3
import json
import os
from colorama import Fore, Style, init

init(autoreset=True)
engine = pyttsx3.init()

HISTORY_FILE = "search_history.json"
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def save_to_history(word):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    history.append(word)
    history = list(set(history))[-10:]  

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def fetch_word_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        word_data = data[0]
        
        print(Fore.CYAN + "\n" + pyfiglet.figlet_format(word, font="slant"))
        print(Fore.YELLOW + f"Word: {word_data['word'].capitalize()}")

        phonetic_text = "N/A"
        phonetic_audio = None
        if "phonetics" in word_data and word_data["phonetics"]:
            for phonetic in word_data["phonetics"]:
                if "text" in phonetic:
                    phonetic_text = phonetic["text"]
                if "audio" in phonetic and phonetic["audio"]:
                    phonetic_audio = phonetic["audio"]

        print(Fore.GREEN + f"Phonetics: {phonetic_text}")
        if phonetic_audio:
            print(Fore.MAGENTA + f"🔊 Pronunciation: {phonetic_audio}")

        
        for meaning in word_data["meanings"]:
            print(Fore.BLUE + f"\n🟢 Part of Speech: {meaning['partOfSpeech']}")
            for definition in meaning["definitions"]:
                print(Fore.WHITE + f" - {definition['definition']}")
                if "example" in definition:
                    print(Fore.LIGHTBLACK_EX + f"   📖 Example: {definition['example']}")

        
        synonyms = meaning.get("synonyms", [])
        antonyms = meaning.get("antonyms", [])
        print(Fore.LIGHTCYAN_EX + "\n🟡 Synonyms:", ", ".join(synonyms) if synonyms else "None")
        print(Fore.LIGHTRED_EX + "🔴 Antonyms:", ", ".join(antonyms) if antonyms else "None")

       
        print(Fore.YELLOW + f"\n🔗 More info: {word_data.get('sourceUrls', ['N/A'])[0]}")

       
        save_to_history(word)

        
        engine.say(f"The word {word} means {word_data['meanings'][0]['definitions'][0]['definition']}")
        engine.runAndWait()

    else:
        print(Fore.RED + "\nWord not found! Suggesting similar words...\n")

      
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

        suggestions = difflib.get_close_matches(word, history, n=3)
        print(Fore.CYAN + "Did you mean:", ", ".join(suggestions) if suggestions else "No suggestions available.")

def fetch_random_word():
    print(Fore.LIGHTMAGENTA_EX + "\n🌟 Word of the Day: 'Serendipity'")  # Placeholder
    fetch_word_meaning("serendipity")

while True:
    print(Fore.YELLOW + "\n💡 MENU: 1. Search Word | 2. Word of the Day | 3. View History | 4. Exit")
    choice = input(Fore.CYAN + "Choose an option: ")

    if choice == "1":
        word = input(Fore.GREEN + "Enter a word: ")
        fetch_word_meaning(word)
    elif choice == "2":
        fetch_random_word()
    elif choice == "3":
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
        print(Fore.LIGHTWHITE_EX + "\n📜 Search History:", ", ".join(history) if history else "No history yet.")
    elif choice == "4":
        print(Fore.RED + "Exiting... Goodbye! 👋")
        break
    else:
        print(Fore.RED + "Invalid choice! Try again.")