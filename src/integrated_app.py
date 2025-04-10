"""
Integration module for the Qur'anic Verse Application.

This module integrates all components and controllers for the application.
"""

import tkinter as tk
from tkinter import ttk

from src.ui_controller import UIController
from src.simulation_controller import SimulationController
from src.advanced_controller import AdvancedController
from src.verse_manager import VerseManager
from src.config_manager import ConfigurationManager

class IntegratedApplication:
    """
    Integrated application that combines all components and controllers.
    """
    
    def __init__(self, root):
        """
        Initialize the integrated application.
        
        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.verse_manager = VerseManager()
        self.config_manager = ConfigurationManager()
        
        # Set up the UI
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the main user interface."""
        # Configure the root window
        self.root.title("Qur'anic Verse Application")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header frame
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create mode selection tabs
        self.mode_tabs = ttk.Notebook(self.header_frame)
        self.mode_tabs.pack(fill=tk.X)
        
        # Create tab frames
        self.standard_tab = ttk.Frame(self.mode_tabs)
        self.simulation_tab = ttk.Frame(self.mode_tabs)
        self.advanced_tab = ttk.Frame(self.mode_tabs)
        
        # Add tabs to notebook
        self.mode_tabs.add(self.standard_tab, text="Standard Mode")
        self.mode_tabs.add(self.simulation_tab, text="Simulation Mode")
        self.mode_tabs.add(self.advanced_tab, text="Advanced Mode 🔒")
        
        # Create content frames for each mode
        self.standard_frame = ttk.Frame(self.main_frame)
        self.simulation_frame = ttk.Frame(self.main_frame)
        self.advanced_frame = ttk.Frame(self.main_frame)
        
        # Initialize controllers
        self.standard_controller = UIController(self.standard_frame)
        self.simulation_controller = SimulationController(
            self.simulation_frame, 
            self.verse_manager, 
            self.config_manager
        )
        self.advanced_controller = AdvancedController(
            self.advanced_frame, 
            self.verse_manager, 
            self.config_manager
        )
        
        # Show standard frame by default
        self.current_mode = "standard"
        self._show_standard_mode()
        
        # Bind tab change event
        self.mode_tabs.bind("<<NotebookTabChanged>>", self._on_tab_changed)
    
    def _show_standard_mode(self):
        """Show the standard mode UI."""
        # Hide other frames
        self.simulation_frame.pack_forget()
        self.advanced_frame.pack_forget()
        
        # Show standard frame
        self.standard_frame.pack(fill=tk.BOTH, expand=True)
        
        # Update current mode
        self.current_mode = "standard"
        
        # Select the standard tab
        self.mode_tabs.select(0)
    
    def _show_simulation_mode(self):
        """Show the simulation mode UI."""
        # Hide other frames
        self.standard_frame.pack_forget()
        self.advanced_frame.pack_forget()
        
        # Show simulation frame
        self.simulation_frame.pack(fill=tk.BOTH, expand=True)
        
        # Update current mode
        self.current_mode = "simulation"
    
    def _show_advanced_mode(self):
        """Show the advanced mode UI."""
        # Hide other frames
        self.standard_frame.pack_forget()
        self.simulation_frame.pack_forget()
        
        # Show advanced frame
        self.advanced_frame.pack(fill=tk.BOTH, expand=True)
        
        # Update current mode
        self.current_mode = "advanced"
    
    def _on_tab_changed(self, event):
        """
        Handle tab change events.
        
        Args:
            event: The tab change event.
        """
        selected_tab = self.mode_tabs.index(self.mode_tabs.select())
        
        if selected_tab == 0:
            self._show_standard_mode()
        elif selected_tab == 1:
            self._show_simulation_mode()
        elif selected_tab == 2:
            self._show_advanced_mode()


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = IntegratedApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
