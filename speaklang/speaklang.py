#!/usr/bin/env python3

import time
import requests
import speech_recognition as sr
from gtts import gTTS
import os
from icecream import ic
import argparse

# Function to send input to ChatGPT API and get response
def get_chatgpt_response(user_input):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY is not set in the environment."

    question_to_chatgpt = f"If I said '{user_input}' how would you respond?"

    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo-0125",
        "messages": [
            {"role": "system", "content": "You are having a conversation with me in French. Just give your response as if talking naturally."},
            {"role": "user", "content": question_to_chatgpt}
        ]
    }
    response = requests.post(endpoint, json=data, headers=headers)
    response_data = response.json()
    if "choices" in response_data:
        return response_data["choices"][0]["message"]["content"]
    elif "completions" in response_data:
        return response_data["completions"][0]["data"]["text"]
    else:
        print("<<<<<<<<<<<<<<<<<<<<")
        print(response_data)
        print(">>>>>>>>>>>>>>>>>>>>")
        return "Error: Unexpected response format from ChatGPT API"

# Function to convert text to speech
def speak(text):
    tts = gTTS(text=text, lang="fr")
    tts.save("response.mp3")
    os.system("afplay response.mp3")  # macOS command for playing audio

# Main loop
def main(debug=False):
    if debug:
        ic.enable()
    else:
        ic.disable()

    r = sr.Recognizer()
    mic = sr.Microphone()

    print("À l'écoute de l'entrée... (dire 'sortie' pour quitter)")
    while True:
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            print("Processing audio...")
            try:
                user_input = r.recognize_google(audio, language="fr-FR")
                if user_input.lower() == "sortie":
                    print("Au revoir!")
                    break
                print(f"User said: {user_input}")
                ic(user_input)

                # Get response from ChatGPT
                response = get_chatgpt_response(user_input)
                ic(response)
                print(f"ChatGPT responded: {response}")

                # Convert ChatGPT response to speech
                speak(response)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"API request error: {e}. Retrying...")
                time.sleep(1)  # Retry after a short delay
        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SpeakLang: A ChatGPT-powered language conversation tool.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    main(debug=args.debug)
