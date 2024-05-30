



import speech_recognition as sr  # Importing the SpeechRecognition library as sr
from langdetect import detect  # Importing the detect function from langdetect module
from googletrans import Translator  # Importing Translator class from googletrans module
from gtts import gTTS  # Importing gTTS class from gtts module for text-to-speech conversion
from playsound import playsound  # Importing playsound function from playsound module for playing audio files

# Supported languages with reversed key-value pairs
languages = {
    'Afrikaans': 'af', 'Arabic': 'ar', 
    'Bangla': 'bn', 'Bulgarian': 'bg', 
    'Catalan': 'ca', 'Czech': 'cs', 
    'Danish': 'da', 'German': 'de', 
    'Greek': 'el', 'English': 'en', 'Esperanto': 'eo', 'Spanish': 'es', 'Estonian': 'et', 
    'Finnish': 'fi', 'French': 'fr',
    'Hindi': 'hi', 'Croatian': 'hr', 'Hungarian': 'hu', 
    'Italian': 'it', 'Indonesian': 'id', 'Icelandic': 'is', 'Hebrew': 'he',
    'Japanese': 'ja', 
    'Korean': 'ko', 
    'Latin': 'la', 'Lithuanian': 'lt', 'Latvian': 'lv',
    'Macedonian': 'mk', 'Malay': 'ms', 'Maltese': 'mt',
    'Dutch': 'nl', 'Norwegian': 'no',
    'Polish': 'pl', 'Portuguese': 'pt', 
    'Romanian': 'ro', 'Russian': 'ru',
    'Slovak': 'sk', 'Slovenian': 'sl', 'Albanian': 'sq', 'Serbian': 'sr', 'Swedish': 'sv', 'Swahili': 'sw',
    'Thai': 'th', 'Tagalog': 'tl', 'Turkish': 'tr', 
    'Ukrainian': 'uk', 'Urdu': 'ur', 
    'Vietnamese': 'vi',
    'Chinese (Simplified)': 'zh-cn', 'Chinese (Traditional)': 'zh-tw'
}

def browse_languages(prompt):
    """
    Function to browse and select a language.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: The language code selected by the user.
    """
    print(prompt)
    while True:
        search_term = input("Enter the language you're looking for: ").strip().capitalize()  # Prompt user to enter the language name
        filtered_languages = {key: value for key, value in languages.items() if search_term in key or search_term in value}  # Filter languages based on the search term
        if not filtered_languages:  # If no language found
            print("No language found matching that name or code. Please try again.")  # Print error message
            continue  # Continue to the next iteration of the loop
        print("Available languages:")  # Print available languages
        for key, value in filtered_languages.items():  # Iterate over filtered languages
            print(f"{key}: {value}")  # Print language name and code
        lang_input = input("Enter the language name or code: ").strip()  # Prompt user to enter language name or code
        if lang_input.capitalize() in languages:  # If language name entered
            return languages[lang_input.capitalize()]  # Return language code
        elif lang_input.lower() in languages.values():  # If language code entered
            return lang_input.lower()  # Return language code
        else:  # If invalid input
            print("Invalid language name or code. Please try again.")  # Print error message

# Select input and output languages
input_lang = browse_languages("Select the input language")  # Prompt user to select input language
output_lang = browse_languages("Select the output language")  # Prompt user to select output language

r = sr.Recognizer()  # Create a recognizer object
translator = Translator(service_urls=['translate.google.com'])  # Create a translator object

while True:
    try:
        with sr.Microphone() as source:  # Use microphone as audio source
            print("Listening...")  # Print listening message
            r.adjust_for_ambient_noise(source)  # Adjust recognizer for ambient noise
            audio = r.listen(source)  # Listen for audio input
            print("Audio captured.")  # Print audio captured message

        text = r.recognize_google(audio, language=input_lang)  # Recognize speech using Google Speech Recognition
        print("Recognized text:", text)  # Print recognized text
        detected_lang = detect(text)  # Detect language of the recognized text
        print("Detected language:", detected_lang)  # Print detected language

        if detected_lang == input_lang:  # If detected language matches input language
            translation = translator.translate(text, dest=output_lang)  # Translate text to output language
            print(f"Translated to {output_lang}: {translation.text}")  # Print translated text
            tts = gTTS(translation.text, lang=output_lang)  # Create a gTTS object for text-to-speech conversion
            tts.save("response.mp3")  # Save the audio to a file
            playsound("response.mp3")  # Play the audio
        else:  # If detected language does not match input language
            print(f"Detected language ({detected_lang}) does not match the selected input language ({input_lang}).")  # Print error message

    except sr.UnknownValueError:  # If speech is unintelligible
        print("Google Speech Recognition could not understand audio")  # Print error message
    except sr.RequestError as e:  # If request to Google Speech Recognition service fails
        print(f"Could not request results from Google Speech Recognition service: {e}")  # Print error message
    except Exception as e:  # If any other exception occurs
        print(f"An error occurred: {e}")  # Print error message

