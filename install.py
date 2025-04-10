"""
Installation script for the Qur'anic Verse Application.

This script checks dependencies and sets up the application.
"""

import sys
import subprocess
import os
import platform

def check_python_version():
    """Check if Python version is compatible."""
    required_version = (3, 8)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"Current version: {current_version[0]}.{current_version[1]}")
        return False
    
    print(f"Python version {current_version[0]}.{current_version[1]} is compatible.")
    return True

def check_tkinter():
    """Check if Tkinter is installed."""
    try:
        import tkinter
        print("Tkinter is installed.")
        return True
    except ImportError:
        print("Error: Tkinter is not installed.")
        if platform.system() == "Linux":
            print("You can install it with: sudo apt-get install python3-tk")
        elif platform.system() == "Darwin":  # macOS
            print("You can install it with: brew install python-tk")
        elif platform.system() == "Windows":
            print("Tkinter should be included with Python. Try reinstalling Python.")
        return False

def install_dependencies():
    """Install required Python packages."""
    required_packages = ["requests"]
    
    print("Installing required packages...")
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to install {package}")
            return False
    
    return True

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ["logs", "config"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
    
    return True

def main():
    """Main installation function."""
    print("=== Qur'anic Verse Application Installation ===")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check Tkinter
    if not check_tkinter():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    print("\nInstallation completed successfully!")
    print("You can now run the application with: python main.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
