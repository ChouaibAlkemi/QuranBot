"""
Configuration Manager for Qur'anic Verse Application

This module handles user preferences and settings.
"""

import json
import os
import hashlib

class ConfigurationManager:
    """
    Manager for handling application configuration and user preferences.
    """
    
    DEFAULT_CONFIG = {
        "language": "en",
        "translation": "en.asad",
        "theme": "light",
        "fontSize": "medium",
        "simulationSpeed": 1.0,
        "advancedModeEnabled": False,
        "advancedModePassword": "",  # Hashed password will be stored here
        "commentDelay": 10,
        "autoScrollDelay": 5,
        "showArabicText": True,
        "showTranslation": True,
        "showReference": True,
        "maxHistorySize": 50
    }
    
    def __init__(self, config_file="config.json"):
        """
        Initialize the configuration manager.
        
        Args:
            config_file (str): Path to the configuration file.
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """
        Load configuration from file or create default if not exists.
        
        Returns:
            dict: Configuration data.
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Ensure all default keys exist
                for key, value in self.DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                
                return config
            except Exception as e:
                print(f"Error loading configuration: {str(e)}")
                return self.DEFAULT_CONFIG.copy()
        else:
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Save the current configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving configuration: {str(e)}")
            return False
    
    def get_config(self):
        """
        Get the current configuration.
        
        Returns:
            dict: Configuration data.
        """
        return self.config.copy()
    
    def update_config(self, updates):
        """
        Update configuration with new values.
        
        Args:
            updates (dict): Dictionary of configuration updates.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            for key, value in updates.items():
                if key in self.config:
                    self.config[key] = value
            
            return self.save_config()
        except Exception as e:
            print(f"Error updating configuration: {str(e)}")
            return False
    
    def reset_to_defaults(self):
        """
        Reset configuration to default values.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        self.config = self.DEFAULT_CONFIG.copy()
        return self.save_config()
    
    def set_advanced_mode_password(self, password):
        """
        Set the password for advanced mode access.
        
        Args:
            password (str): The password to set.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Hash the password for security
            hashed = hashlib.sha256(password.encode()).hexdigest()
            self.config["advancedModePassword"] = hashed
            return self.save_config()
        except Exception as e:
            print(f"Error setting password: {str(e)}")
            return False
    
    def verify_advanced_mode_password(self, password):
        """
        Verify the advanced mode password.
        
        Args:
            password (str): The password to verify.
        
        Returns:
            bool: True if password is correct, False otherwise.
        """
        stored_hash = self.config.get("advancedModePassword", "")
        
        if not stored_hash:
            return False
            
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        return input_hash == stored_hash
    
    def enable_advanced_mode(self, password):
        """
        Enable advanced mode with password verification.
        
        Args:
            password (str): The password to verify.
        
        Returns:
            bool: True if enabled successfully, False otherwise.
        """
        if self.verify_advanced_mode_password(password):
            self.config["advancedModeEnabled"] = True
            return self.save_config()
        return False
    
    def disable_advanced_mode(self):
        """
        Disable advanced mode.
        
        Returns:
            bool: True if disabled successfully, False otherwise.
        """
        self.config["advancedModeEnabled"] = False
        return self.save_config()
    
    def is_advanced_mode_enabled(self):
        """
        Check if advanced mode is enabled.
        
        Returns:
            bool: True if advanced mode is enabled, False otherwise.
        """
        return self.config.get("advancedModeEnabled", False)


# Simple test function
def test_config_manager():
    """Test the configuration manager functionality."""
    # Use a test config file
    config_manager = ConfigurationManager("test_config.json")
    
    # Test getting config
    print("Default configuration:")
    print(json.dumps(config_manager.get_config(), indent=2))
    
    # Test updating config
    print("\nUpdating configuration...")
    updates = {
        "translation": "en.pickthall",
        "theme": "dark",
        "fontSize": "large"
    }
    success = config_manager.update_config(updates)
    print(f"Update successful: {success}")
    print("Updated configuration:")
    print(json.dumps(config_manager.get_config(), indent=2))
    
    # Test password functionality
    print("\nTesting password functionality...")
    config_manager.set_advanced_mode_password("test123")
    print(f"Correct password verification: {config_manager.verify_advanced_mode_password('test123')}")
    print(f"Incorrect password verification: {config_manager.verify_advanced_mode_password('wrong')}")
    
    # Test enabling advanced mode
    print("\nEnabling advanced mode...")
    print(f"With correct password: {config_manager.enable_advanced_mode('test123')}")
    print(f"Advanced mode enabled: {config_manager.is_advanced_mode_enabled()}")
    
    # Clean up test file
    if os.path.exists("test_config.json"):
        os.remove("test_config.json")
        print("\nTest config file removed.")


if __name__ == "__main__":
    test_config_manager()
