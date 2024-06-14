#!/usr/bin/env python3

import requests
import speech_recognition as sr
from gtts import gTTS
import os

# Function to send input to ChatGPT API and get response
def get_chatgpt_response(user_input):
    # get chatgpt api ket from env var
    api_key = os.environ.get("OPENAI_API_KEY")

    question_to_chatgpt = f"If I said '{user_input}' how would you respond?"

    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo-0125",
        "messages": [
            {"role": "system", "content": "You are having a conversation with me in french. Just give your response as if talking naturally"},
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
def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("À l'écoute de l'entrée... (dire 'sortie' pour quitter)")
        while True:
            try:
                audio = r.listen(source)
                user_input = r.recognize_google(audio, language="fr-FR")
                print(f"User said: {user_input}")
                if user_input.lower() == "sortie":
                    break
                response = get_chatgpt_response(user_input)
                print(f"ChatGPT responded: {response}")
                speak(response)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Error fetching results; {e}")

if __name__ == "__main__":
    main()
