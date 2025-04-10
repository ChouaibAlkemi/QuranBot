"""
API Service for Qur'anic Verse Application

This module handles communication with the AlQuran.cloud API.
"""

import random
import requests
import json
import time

class APIService:
    """
    Service for interacting with the AlQuran.cloud API.
    """
    
    BASE_URL = "http://api.alquran.cloud/v1"
    TOTAL_VERSES = 6236
    
    def __init__(self):
        """Initialize the API service."""
        self.cache = {}
        self.last_request_time = 0
        
    def _rate_limit(self):
        """Simple rate limiting to avoid overwhelming the API."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < 1.0:  # Ensure at least 1 second between requests
            time.sleep(1.0 - time_since_last)
            
        self.last_request_time = time.time()
    
    def get_random_verse(self, editions=None):
        """
        Get a random verse from the Quran.
        
        Args:
            editions (str, optional): Comma-separated list of edition identifiers.
                                     Defaults to "quran-uthmani,en.asad".
        
        Returns:
            dict: The verse data or None if an error occurred.
        """
        if editions is None:
            editions = "quran-uthmani,en.asad"
            
        random_ayah_number = random.randint(1, self.TOTAL_VERSES)
        cache_key = f"{random_ayah_number}_{editions}"
        
        # Check if we have this verse cached
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Apply rate limiting
        self._rate_limit()
        
        try:
            url = f"{self.BASE_URL}/ayah/{random_ayah_number}/editions/{editions}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "OK":
                    # Cache the result
                    self.cache[cache_key] = data["data"]
                    return data["data"]
                else:
                    print(f"API returned non-OK status: {data['status']}")
                    return None
            else:
                print(f"API request failed with status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error fetching random verse: {str(e)}")
            return None
    
    def get_specific_verse(self, reference, editions=None):
        """
        Get a specific verse from the Quran.
        
        Args:
            reference (str): Verse reference (number or surah:ayah format).
            editions (str, optional): Comma-separated list of edition identifiers.
                                     Defaults to "quran-uthmani,en.asad".
        
        Returns:
            dict: The verse data or None if an error occurred.
        """
        if editions is None:
            editions = "quran-uthmani,en.asad"
            
        cache_key = f"{reference}_{editions}"
        
        # Check if we have this verse cached
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Apply rate limiting
        self._rate_limit()
        
        try:
            url = f"{self.BASE_URL}/ayah/{reference}/editions/{editions}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "OK":
                    # Cache the result
                    self.cache[cache_key] = data["data"]
                    return data["data"]
                else:
                    print(f"API returned non-OK status: {data['status']}")
                    return None
            else:
                print(f"API request failed with status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error fetching specific verse: {str(e)}")
            return None
    
    def get_available_editions(self):
        """
        Get a list of all available editions (translations and recitations).
        
        Returns:
            list: List of available editions or None if an error occurred.
        """
        # Check if we have editions cached
        if "editions" in self.cache:
            return self.cache["editions"]
        
        # Apply rate limiting
        self._rate_limit()
        
        try:
            url = f"{self.BASE_URL}/edition"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "OK":
                    # Cache the result
                    self.cache["editions"] = data["data"]
                    return data["data"]
                else:
                    print(f"API returned non-OK status: {data['status']}")
                    return None
            else:
                print(f"API request failed with status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error fetching editions: {str(e)}")
            return None
    
    def clear_cache(self):
        """Clear the API cache."""
        self.cache = {}


# Simple test function
def test_api_service():
    """Test the API service functionality."""
    api = APIService()
    
    # Test getting a random verse
    print("Testing random verse retrieval...")
    verse = api.get_random_verse()
    if verse:
        print(f"Successfully retrieved verse {verse['number']}")
        for edition in verse['edition']:
            if 'text' in edition:
                print(f"{edition['identifier']}: {edition['text']}")
    else:
        print("Failed to retrieve random verse")
    
    # Test getting available editions
    print("\nTesting editions retrieval...")
    editions = api.get_available_editions()
    if editions:
        print(f"Successfully retrieved {len(editions)} editions")
        print("First 5 editions:")
        for i, edition in enumerate(editions[:5]):
            print(f"{i+1}. {edition['name']} ({edition['identifier']})")
    else:
        print("Failed to retrieve editions")


if __name__ == "__main__":
    test_api_service()
