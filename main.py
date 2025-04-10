"""
Main Application for Qur'anic Verse Display

This module serves as the entry point for the Qur'anic Verse Application.
"""

import tkinter as tk
from src.ui_controller import UIController

def main():
    """Main function to run the application."""
    root = tk.Tk()
    root.title("Qur'anic Verse Application")
    
    # Set icon (if available)
    try:
        root.iconbitmap("assets/icon.ico")
    except:
        pass
    
    # Initialize the UI controller
    app = UIController(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
