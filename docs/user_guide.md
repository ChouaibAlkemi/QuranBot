# Qur'anic Verse Application - User Guide

## Overview

The Qur'anic Verse Application is an educational tool that allows you to explore Qur'anic verses in multiple ways. The application features three distinct modes:

1. **Standard Mode**: A simple interface for viewing random Qur'anic verses with translations
2. **Simulation Mode**: An educational demonstration that simulates automation workflow
3. **Advanced Developer Mode**: A local sandbox environment for hands-on learning about automation concepts

This application is designed for educational purposes only and operates entirely within a local environment.

## Installation

### Prerequisites

- Python 3.8 or higher
- Tkinter (usually included with Python)
- Internet connection (for API access)

### Installation Steps

1. Clone or download the repository to your local machine
2. Navigate to the project directory
3. Install required dependencies:

```bash
pip install requests
```

## Running the Application

To start the application, run the following command from the project directory:

```bash
python main.py
```

## Features

### Standard Mode

The Standard Mode provides a clean, user-friendly interface for exploring Qur'anic verses:

- **Random Verse Generation**: Fetch random verses from the Quran
- **Multiple Translations**: Choose from various available translations
- **Copy and Share**: Easily copy verses to clipboard or share them
- **Theme Options**: Switch between light and dark themes

#### How to Use Standard Mode

1. Click the "New Random Verse" button to fetch a random verse
2. Use the translation dropdown to select your preferred translation
3. Click "Copy" to copy the verse to your clipboard
4. Click "Share" to see sharing options

### Simulation Mode

The Simulation Mode provides an educational demonstration of how automation workflows function:

- **Simulated Content Feed**: A mock social media feed for demonstration
- **Visual Automation**: Step-by-step visualization of automation processes
- **Adjustable Speed**: Control the simulation speed
- **Progress Tracking**: Monitor the simulation progress

#### How to Use Simulation Mode

1. Click the "Simulation Mode" tab
2. Click "Start Simulation" to begin the demonstration
3. Use the speed slider to adjust the simulation speed
4. Click "Pause" to pause the simulation or "Reset" to start over
5. Watch as the simulation scrolls through posts, fetches verses, and adds comments

### Advanced Developer Mode (Educational)

The Advanced Developer Mode provides a hands-on sandbox environment for learning about automation concepts:

- **Local Sandbox**: Fully functional automation within a controlled environment
- **Real-time Statistics**: Track posts processed, comments made, and API calls
- **Execution Controls**: Start, pause, and stop execution
- **Detailed Logging**: Monitor all actions in real-time

#### How to Use Advanced Developer Mode

1. Click the "Advanced Mode" tab
2. Click "Unlock Advanced Mode" and enter the password (set in Settings)
3. Adjust the comment delay as desired
4. Click "Start Execution" to begin the automation
5. Monitor the statistics and logs as the automation runs
6. Use "Pause" or "Stop" to control the execution

## Configuration

### Settings

Access the settings by clicking the gear icon (⚙️) in the top-right corner:

- **General Settings**:
  - Theme: Choose between light and dark themes
  - Font Size: Adjust the text size

- **Advanced Settings**:
  - Set Password: Create a password for Advanced Mode access
  - Warning: Reminder about educational use only

### Translation Options

The application uses the AlQuran.cloud API which provides multiple translations:

- Muhammad Asad (default)
- Pickthall
- Yusuf Ali
- And many others available in the dropdown

## Educational Purpose

This application is designed for educational purposes only, specifically to:

1. Learn about API integration and data retrieval
2. Understand automation concepts in a controlled environment
3. Study user interface design and implementation
4. Explore ethical considerations in automation

The Advanced Developer Mode is provided solely as an educational tool to demonstrate automation concepts within a local sandbox environment. It is not intended for use in creating tools that interact with actual social media platforms or violate any platform's terms of service.

## Troubleshooting

### Common Issues

- **No Internet Connection**: The application requires internet access to fetch verses from the API
- **API Rate Limiting**: If you encounter errors, you may have exceeded the API rate limit; wait a few minutes and try again
- **Display Issues**: If text appears cut off, try adjusting the window size or font settings

### Error Reporting

If you encounter any bugs or issues, please report them by creating an issue in the project repository.

## Technical Details

### API Information

The application uses the AlQuran.Cloud API:
- Base URL: http://api.alquran.cloud/v1
- No authentication required
- Rate limiting may apply

### File Structure

```
facebook_quran_commenter/
├── main.py                  # Main entry point
├── src/
│   ├── api_service.py       # API communication
│   ├── verse_manager.py     # Verse handling
│   ├── config_manager.py    # Configuration
│   ├── ui_controller.py     # Standard mode UI
│   ├── simulation_controller.py  # Simulation mode
│   ├── advanced_controller.py    # Advanced mode
│   └── integrated_app.py    # Integration
├── tests/
│   ├── test_components.py   # Unit tests
│   └── test_integration.py  # Integration tests
└── docs/
    └── user_guide.md        # This document
```

## License

This project is released under the MIT License. See the LICENSE file for details.

## Acknowledgments

- AlQuran.Cloud API for providing Qur'anic content
- The Islamic Network for their valuable resources
- All contributors to the project

---

*This application was created for educational purposes only. It is not affiliated with any social media platform.*
