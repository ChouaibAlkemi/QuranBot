"""
Verse Manager for Qur'anic Verse Application

This module manages verse retrieval, formatting, and caching.
"""

from src.api_service import APIService

class VerseManager:
    """
    Manager for handling Qur'anic verses.
    """

    def __init__(self):
        """Initialize the verse manager."""
        self.api_service = APIService()
        self.current_verse = None
        self.history = []
        self.max_history = 50

    def get_random_verse(self, translation="en.asad"):
        """
        Get a random verse with the specified translation.
        
        Args:
            translation (str): The translation identifier.
        
        Returns:
            dict: Formatted verse data.
        """
        editions = f"quran-uthmani,{translation}"
        verse_data = self.api_service.get_random_verse(editions)

        if verse_data:
            formatted_verse = self._format_verse(verse_data)
            self.current_verse = formatted_verse
            self._add_to_history(formatted_verse)
            return formatted_verse

        return None

    def get_specific_verse(self, reference, translation="en.asad"):
        """
        Get a specific verse with the specified translation.
        
        Args:
            reference (str): Verse reference (number or surah:ayah format).
            translation (str): The translation identifier.
        
        Returns:
            dict: Formatted verse data.
        """
        editions = f"quran-uthmani,{translation}"
        verse_data = self.api_service.get_specific_verse(reference, editions)

        if verse_data:
            formatted_verse = self._format_verse(verse_data)
            self.current_verse = formatted_verse
            self._add_to_history(formatted_verse)
            return formatted_verse

        return None

    def _format_verse(self, verse_data):
        """
        Format the verse data into a standardized structure.

        Args:
            verse_data (dict or list): Raw verse data from the API.

        Returns:
            dict: Formatted verse data.
        """
        if not isinstance(verse_data, list):
            verse_data = [verse_data]

        formatted_verse = {
            "number": None,
            "surah": {
                "number": None,
                "name": None,
                "englishName": None
            },
            "text": {
                "arabic": None,
                "translation": None
            },
            "audio": {
                "url": None
            },
            "reference": None
        }

        for entry in verse_data:
            edition_info = entry.get("edition", {})
            identifier = edition_info.get("identifier")

            if identifier == "quran-uthmani":
                formatted_verse["text"]["arabic"] = entry.get("text")
                surah = entry.get("surah", {})
                formatted_verse["surah"]["number"] = surah.get("number")
                formatted_verse["surah"]["name"] = surah.get("name")
                formatted_verse["surah"]["englishName"] = surah.get("englishName")
                formatted_verse["reference"] = f"{surah.get('number')}:{entry.get('numberInSurah')}"
                formatted_verse["number"] = entry.get("number")

            elif identifier:
                formatted_verse["text"]["translation"] = entry.get("text")

            if entry.get("audio"):
                formatted_verse["audio"]["url"] = entry["audio"]

        return formatted_verse

    def _add_to_history(self, verse):
        """
        Add a verse to the history.
        
        Args:
            verse (dict): Formatted verse data.
        """
        self.history.append(verse)

        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_available_translations(self):
        """
        Get a list of available translations.
        
        Returns:
            list: List of translation editions.
        """
        editions = self.api_service.get_available_editions()

        if editions:
            translations = [
                {
                    "identifier": edition["identifier"],
                    "language": edition["language"],
                    "name": edition["name"],
                    "englishName": edition.get("englishName", edition["name"])
                }
                for edition in editions
                if edition["format"] == "text" and edition["type"] == "translation"
            ]
            return translations

        return []

    def get_available_recitations(self):
        """
        Get a list of available audio recitations.
        
        Returns:
            list: List of audio editions.
        """
        editions = self.api_service.get_available_editions()

        if editions:
            recitations = [
                {
                    "identifier": edition["identifier"],
                    "language": edition["language"],
                    "name": edition["name"],
                    "englishName": edition.get("englishName", edition["name"])
                }
                for edition in editions
                if edition["format"] == "audio"
            ]
            return recitations

        return []

    def get_verse_history(self):
        """
        Get the verse history.
        
        Returns:
            list: List of verses in the history.
        """
        return self.history

    def clear_history(self):
        """Clear the verse history."""
        self.history = []

    def get_formatted_verse_text(self, verse=None, include_reference=True):
        """
        Get a formatted string representation of a verse.
        
        Args:
            verse (dict, optional): Verse data. Defaults to current verse.
            include_reference (bool): Whether to include the reference.
        
        Returns:
            str: Formatted verse text.
        """
        if verse is None:
            verse = self.current_verse

        if verse is None:
            return "No verse available."

        arabic = verse["text"]["arabic"]
        translation = verse["text"]["translation"]

        if include_reference:
            surah_name = verse["surah"]["englishName"]
            reference = verse["reference"]
            return f"﴾ {arabic} ﴿\n\n{translation}\n\n— Surah {surah_name} ({reference})"
        else:
            return f"﴾ {arabic} ﴿\n\n{translation}"

# Simple test function
def test_verse_manager():
    """Test the verse manager functionality."""
    manager = VerseManager()

    print("Testing random verse retrieval...")
    verse = manager.get_random_verse()
    if verse:
        print("Successfully retrieved random verse:")
        print(manager.get_formatted_verse_text(verse))
    else:
        print("Failed to retrieve random verse")

    print("\nTesting translations retrieval...")
    translations = manager.get_available_translations()
    if translations:
        print(f"Successfully retrieved {len(translations)} translations")
        print("First 5 translations:")
        for i, translation in enumerate(translations[:5]):
            print(f"{i+1}. {translation['englishName']} ({translation['identifier']})")
    else:
        print("Failed to retrieve translations")

if __name__ == "__main__":
    test_verse_manager()
