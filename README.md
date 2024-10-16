# SpeakLang

## Overview

**SpeakLang** is an interactive program that listens to spoken input in French, sends it to the ChatGPT API for processing, and vocalizes the AI's response. This allows users to engage in a spoken chat entirely in French, making it an excellent tool for language learners and conversational practice.

## Features

- **Speech Recognition**: Utilizes the Google Speech Recognition API to convert spoken language into text.
- **ChatGPT Integration**: Communicates with the ChatGPT API to generate responses based on user input.
- **Text-to-Speech**: Uses Google Text-to-Speech (gTTS) to convert AI-generated responses back to audio in French.
- **Interactive Interface**: A voice-activated chat interface that remains active until the user commands it to exit by saying "sortie".

## Requirements

This project requires Python 3 and the following packages:

- `requests`
- `speech_recognition`
- `gTTS`
- `PyAudio` (for microphone input)

You can install the dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Environment Setup

1. **Python Installation**: Ensure you have Python 3 installed on your system.

2. **API Key Configuration**: Obtain your OpenAI API key and set it as an environment variable:

   ```bash
   export OPENAI_API_KEY='your_api_key_here'
   ```

3. **Installing Dependencies**: Run the following command in your terminal to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the application, run the main Python script:

```bash
python3 speaklang/speaklang.py
```

Once running, the program will listen for your input. Speak naturally in French, and the program will respond accordingly. To exit the application, simply say "sortie".

## Running Tests

To ensure the functionality of SpeakLang, you can run the included unit tests with:

```bash
python3 -m unittest discover -s tests
```

## Contributing

We welcome contributions! Please fork the repository and create a pull request for any enhancements, features, or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [OpenAI](https://openai.com) for providing the ChatGPT API.
- [Google](https://g.co/doodle) for the Text-to-Speech API.
- The [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library for enabling speech recognition capabilities.

## Support

If you encounter any issues or have questions, feel free to open an issue in this repository or contact the maintainers.
