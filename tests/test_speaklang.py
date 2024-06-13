#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
from speaklang.speaklang import get_chatgpt_response, speak  # Importing directly from the module

class TestSpeakLang(unittest.TestCase):
    @patch('speaklang.speaklang.requests.post')  # Patching the correct path to requests
    def test_get_chatgpt_response(self, mock_post):
        # Mock response data
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

    @patch('speaklang.speaklang.gTTS')  # Patching the correct path to gTTS
    @patch('speaklang.speaklang.os.system')  # Patching the correct path to os.system
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

if __name__ == '__main__':
    unittest.main()

