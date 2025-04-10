"""
Test script for the Qur'anic Verse Application.

This script tests the functionality of all components and modes.
"""

import unittest
import tkinter as tk
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api_service import APIService
from src.verse_manager import VerseManager
from src.config_manager import ConfigurationManager

class TestAPIService(unittest.TestCase):
    """Test cases for the API Service."""
    
    def setUp(self):
        """Set up test environment."""
        self.api_service = APIService()
    
    @patch('src.api_service.requests.get')
    def test_get_random_verse(self, mock_get):
        """Test getting a random verse."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "status": "OK",
            "data": {
                "number": 262,
                "edition": [
                    {
                        "identifier": "quran-uthmani",
                        "language": "ar",
                        "name": "Uthmani",
                        "text": "Arabic text",
                        "surah": {
                            "number": 2,
                            "name": "سورة البقرة",
                            "englishName": "Al-Baqarah"
                        },
                        "numberInSurah": 255
                    },
                    {
                        "identifier": "en.asad",
                        "language": "en",
                        "name": "Muhammad Asad",
                        "text": "English translation"
                    }
                ]
            }
        }
        mock_get.return_value = mock_response
        
        # Test
        verse = self.api_service.get_random_verse()
        
        # Assertions
        self.assertIsNotNone(verse)
        self.assertEqual(verse["number"], 262)
        self.assertEqual(len(verse["edition"]), 2)
        
        # Verify API call
        mock_get.assert_called_once()
        self.assertIn("ayah", mock_get.call_args[0][0])
    
    @patch('src.api_service.requests.get')
    def test_get_specific_verse(self, mock_get):
        """Test getting a specific verse."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "status": "OK",
            "data": {
                "number": 1,
                "edition": [
                    {
                        "identifier": "quran-uthmani",
                        "language": "ar",
                        "name": "Uthmani",
                        "text": "Arabic text",
                        "surah": {
                            "number": 1,
                            "name": "سورة الفاتحة",
                            "englishName": "Al-Fatiha"
                        },
                        "numberInSurah": 1
                    },
                    {
                        "identifier": "en.asad",
                        "language": "en",
                        "name": "Muhammad Asad",
                        "text": "English translation"
                    }
                ]
            }
        }
        mock_get.return_value = mock_response
        
        # Test
        verse = self.api_service.get_specific_verse("1:1")
        
        # Assertions
        self.assertIsNotNone(verse)
        self.assertEqual(verse["number"], 1)
        
        # Verify API call
        mock_get.assert_called_once()
        self.assertIn("1:1", mock_get.call_args[0][0])
    
    @patch('src.api_service.requests.get')
    def test_error_handling(self, mock_get):
        """Test error handling."""
        # Mock error response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Test
        verse = self.api_service.get_random_verse()
        
        # Assertions
        self.assertIsNone(verse)


class TestVerseManager(unittest.TestCase):
    """Test cases for the Verse Manager."""
    
    def setUp(self):
        """Set up test environment."""
        self.verse_manager = VerseManager()
        # Mock the API service
        self.verse_manager.api_service = MagicMock()
    
    def test_get_random_verse(self):
        """Test getting a random verse."""
        # Mock API response
        mock_verse = {
            "number": 262,
            "edition": [
                {
                    "identifier": "quran-uthmani",
                    "language": "ar",
                    "name": "Uthmani",
                    "text": "Arabic text",
                    "surah": {
                        "number": 2,
                        "name": "سورة البقرة",
                        "englishName": "Al-Baqarah"
                    },
                    "numberInSurah": 255
                },
                {
                    "identifier": "en.asad",
                    "language": "en",
                    "name": "Muhammad Asad",
                    "text": "English translation"
                }
            ]
        }
        self.verse_manager.api_service.get_random_verse.return_value = mock_verse
        
        # Test
        verse = self.verse_manager.get_random_verse()
        
        # Assertions
        self.assertIsNotNone(verse)
        self.assertEqual(verse["number"], 262)
        self.assertEqual(verse["text"]["arabic"], "Arabic text")
        self.assertEqual(verse["text"]["translation"], "English translation")
        self.assertEqual(verse["reference"], "2:255")
        
        # Verify API call
        self.verse_manager.api_service.get_random_verse.assert_called_once()
    
    def test_get_formatted_verse_text(self):
        """Test getting formatted verse text."""
        # Set up test verse
        test_verse = {
            "number": 1,
            "surah": {
                "number": 1,
                "name": "الفاتحة",
                "englishName": "Al-Fatiha"
            },
            "text": {
                "arabic": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                "translation": "In the name of Allah, the Entirely Merciful, the Especially Merciful."
            },
            "reference": "1:1"
        }
        self.verse_manager.current_verse = test_verse
        
        # Test
        formatted_text = self.verse_manager.get_formatted_verse_text()
        
        # Assertions
        self.assertIn("بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", formatted_text)
        self.assertIn("In the name of Allah", formatted_text)
        self.assertIn("Al-Fatiha", formatted_text)
        self.assertIn("1:1", formatted_text)


class TestConfigManager(unittest.TestCase):
    """Test cases for the Configuration Manager."""
    
    def setUp(self):
        """Set up test environment."""
        # Use a test config file
        self.config_manager = ConfigurationManager("test_config.json")
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove test config file
        if os.path.exists("test_config.json"):
            os.remove("test_config.json")
    
    def test_default_config(self):
        """Test default configuration."""
        config = self.config_manager.get_config()
        
        # Assertions
        self.assertEqual(config["language"], "en")
        self.assertEqual(config["translation"], "en.asad")
        self.assertEqual(config["theme"], "light")
        self.assertFalse(config["advancedModeEnabled"])
    
    def test_update_config(self):
        """Test updating configuration."""
        # Update config
        updates = {
            "translation": "en.pickthall",
            "theme": "dark"
        }
        result = self.config_manager.update_config(updates)
        
        # Assertions
        self.assertTrue(result)
        
        # Get updated config
        config = self.config_manager.get_config()
        self.assertEqual(config["translation"], "en.pickthall")
        self.assertEqual(config["theme"], "dark")
    
    def test_password_functionality(self):
        """Test password functionality."""
        # Set password
        result = self.config_manager.set_advanced_mode_password("test123")
        self.assertTrue(result)
        
        # Verify password
        self.assertTrue(self.config_manager.verify_advanced_mode_password("test123"))
        self.assertFalse(self.config_manager.verify_advanced_mode_password("wrong"))
        
        # Enable advanced mode
        self.assertTrue(self.config_manager.enable_advanced_mode("test123"))
        self.assertTrue(self.config_manager.is_advanced_mode_enabled())
        
        # Disable advanced mode
        self.assertTrue(self.config_manager.disable_advanced_mode())
        self.assertFalse(self.config_manager.is_advanced_mode_enabled())


def run_tests():
    """Run all tests."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


if __name__ == "__main__":
    run_tests()
