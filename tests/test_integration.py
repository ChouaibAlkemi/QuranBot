"""
Integration test script for the Qur'anic Verse Application.

This script tests the integration of all components and modes.
"""

import unittest
import tkinter as tk
from unittest.mock import MagicMock, patch
import sys
import os
import threading
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.integrated_app import IntegratedApplication

class TestIntegratedApplication(unittest.TestCase):
    """Test cases for the Integrated Application."""
    
    def setUp(self):
        """Set up test environment."""
        self.root = tk.Tk()
        self.app = None
    
    def tearDown(self):
        """Clean up after tests."""
        if self.app:
            # Clean up any resources
            pass
        
        # Destroy the root window
        if self.root:
            self.root.destroy()
    
    def test_application_initialization(self):
        """Test application initialization."""
        # Initialize the application
        self.app = IntegratedApplication(self.root)
        
        # Assertions
        self.assertEqual(self.app.current_mode, "standard")
        self.assertIsNotNone(self.app.verse_manager)
        self.assertIsNotNone(self.app.config_manager)
        
        # Check that the tabs are created
        self.assertEqual(self.app.mode_tabs.index("end"), 3)  # 3 tabs
    
    def test_mode_switching(self):
        """Test mode switching."""
        # Initialize the application
        self.app = IntegratedApplication(self.root)
        
        # Test switching to simulation mode
        self.app._show_simulation_mode()
        self.assertEqual(self.app.current_mode, "simulation")
        
        # Test switching to advanced mode
        self.app._show_advanced_mode()
        self.assertEqual(self.app.current_mode, "advanced")
        
        # Test switching back to standard mode
        self.app._show_standard_mode()
        self.assertEqual(self.app.current_mode, "standard")
    
    @patch('src.integrated_app.SimulationController')
    @patch('src.integrated_app.AdvancedController')
    @patch('src.integrated_app.UIController')
    def test_controller_initialization(self, mock_ui, mock_simulation, mock_advanced):
        """Test controller initialization."""
        # Initialize the application
        self.app = IntegratedApplication(self.root)
        
        # Assertions
        mock_ui.assert_called_once()
        mock_simulation.assert_called_once()
        mock_advanced.assert_called_once()


def run_integration_tests():
    """Run all integration tests."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


if __name__ == "__main__":
    run_integration_tests()
