#!/usr/bin/env python3

import unittest
import io
import sys
from unittest.mock import patch, MagicMock
from speaklang.speaklang import get_chatgpt_response, speak, main
import speech_recognition as sr

class TestSpeakLang(unittest.TestCase):
    @patch('speaklang.speaklang.requests.post')
    def test_get_chatgpt_response_choices(self, mock_post):
        # Mock response data with "choices"
        mock_response_data = {
            "choices": [
                {"message": {"content": "Bonjour!"}}
            ]
        }
        # Configure mock to return the mock response data
        mock_post.return_value.json.return_value = mock_response_data

        # Call the function under test
        response = get_chatgpt_response("Bonjour")

        # Check if the function returns the expected response
        self.assertEqual(response, "Bonjour!")

    @patch('speaklang.speaklang.requests.post')
    def test_get_chatgpt_response_completions(self, mock_post):
        # Mock response data with "completions"
        mock_response_data = {
            "completions": [
                {"data": {"text": "Au revoir!"}}
            ]
        }
        # Configure mock to return the mock response data
        mock_post.return_value.json.return_value = mock_response_data

        # Call the function under test
        response = get_chatgpt_response("Au revoir")

        # Check if the function returns the expected response
        self.assertEqual(response, "Au revoir!")

    @patch('speaklang.speaklang.requests.post')
    def test_get_chatgpt_response_unexpected_format(self, mock_post):
        # Mock response data with unexpected format
        mock_response_data = {
            "unexpected_field": "some_value"
        }
        # Configure mock to return the mock response data
        mock_post.return_value.json.return_value = mock_response_data

        # Use patch to capture print output
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            # Call the function under test
            response = get_chatgpt_response("Unexpected")

            # Check if the function prints debug information and returns the error message
            self.assertIn("<<<<<<<<<<<<<<<<<<<<", mock_stdout.getvalue())
            self.assertIn("{'unexpected_field': 'some_value'}", mock_stdout.getvalue())
            self.assertIn(">>>>>>>>>>>>>>>>>>>>", mock_stdout.getvalue())
            self.assertEqual(response, "Error: Unexpected response format from ChatGPT API")

    @patch('speaklang.speaklang.gTTS')
    @patch('speaklang.speaklang.os.system')
    def test_speak(self, mock_os_system, mock_gtts):
        # Mock gTTS object and save method
        mock_tts = MagicMock()
        mock_gtts.return_value = mock_tts
        mock_save = MagicMock()
        mock_tts.save = mock_save

        # Call the function under test
        speak("Bonjour!")

        # Check if the gTTS object is called with the correct parameters
        mock_gtts.assert_called_once_with(text="Bonjour!", lang="fr")
        mock_save.assert_called_once_with("response.mp3")
        mock_os_system.assert_called_once_with("afplay response.mp3")

    @patch('speaklang.speaklang.sr.Recognizer')  # Patching the Recognizer class
    @patch('speaklang.speaklang.get_chatgpt_response')  # Mocking get_chatgpt_response for simplicity
    @patch('speaklang.speaklang.speak')  # Mocking speak function for simplicity
    def test_main_exit_command(self, mock_speak, mock_get_chatgpt_response, MockRecognizer):
        # Create a mock recognizer instance and mock its methods
        mock_recognizer_instance = MockRecognizer.return_value
        mock_listen = mock_recognizer_instance.listen
        mock_recognize_google = mock_recognizer_instance.recognize_google

        # Mock the return values for recognize_google
        mock_recognize_google.side_effect = ["some speech", "sortie"]

        # Call the main function
        with patch('speaklang.speaklang.sr.Microphone'):
            main()

        # Check if speak was called with the expected responses
        mock_get_chatgpt_response.assert_called_with("some speech")
        mock_speak.assert_called_with(mock_get_chatgpt_response.return_value)

        # Check if the main loop exited after recognizing "sortie"
        self.assertTrue(mock_listen.called)
        self.assertEqual(mock_listen.call_count, 2)  # Assuming two calls, one for "some speech" and one for "sortie")

    @patch('speaklang.speaklang.sr.Recognizer')
    @patch('speaklang.speaklang.get_chatgpt_response')
    @patch('speaklang.speaklang.speak')
    def test_main_unknown_value_error(self, mock_speak, mock_get_chatgpt_response, MockRecognizer):
        # Create a mock recognizer instance and mock its methods
        mock_recognizer_instance = MockRecognizer.return_value
        mock_listen = mock_recognizer_instance.listen
        mock_recognize_google = mock_recognizer_instance.recognize_google

        # Mock the return values for recognize_google
        mock_recognize_google.side_effect = ["error speech", "sortie"]

        # Configure get_chatgpt_response to return a string for "error speech"
        mock_get_chatgpt_response.side_effect = [sr.UnknownValueError(), "Error: Unexpected audio input"]

        # Capture stdout output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the main function
        with patch('speaklang.speaklang.sr.Microphone'):
            main()

        # Reset stdout
        sys.stdout = sys.__stdout__

        # Check if "Could not understand audio" message was printed
        self.assertIn("Could not understand audio", captured_output.getvalue())

    @patch('speaklang.speaklang.sr.Recognizer')  # Patching the Recognizer class
    @patch('speaklang.speaklang.get_chatgpt_response')  # Mocking get_chatgpt_response for simplicity
    @patch('speaklang.speaklang.speak')  # Mocking speak function for simplicity
    def test_main_request_error(self, mock_speak, mock_get_chatgpt_response, MockRecognizer):
        # Create a mock recognizer instance and mock its methods
        mock_recognizer_instance = MockRecognizer.return_value
        mock_listen = mock_recognizer_instance.listen
        mock_recognize_google = mock_recognizer_instance.recognize_google

        # Mock the return values for recognize_google
        mock_recognize_google.side_effect = [sr.RequestError("Mock request error"), "sortie"]

        # Capture stdout output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the main function
        with patch('speaklang.speaklang.sr.Microphone'):
            main()

        # Reset stdout
        sys.stdout = sys.__stdout__

        # Check if "Error fetching results;" message with the specific error was printed
        self.assertIn("Error fetching results;", captured_output.getvalue())
        self.assertIn("Mock request error", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()

