# Data Flow and Component Interactions

## Core Data Flows

### 1. Verse Retrieval Flow
```
User Request → UI Controller → Verse Manager → API Service → AlQuran.cloud API
                                    ↑               ↓
                                    └───────────────┘
                                    Return Verse Data
```

### 2. Mode Switching Flow
```
User Selection → UI Controller → Mode Controller → Load Mode-Specific UI
                                      ↓
                                Configuration Manager
                                (Save Preferences)
```

### 3. Configuration Flow
```
User Settings → UI Controller → Configuration Manager → Save Settings
                                        ↓
                                  Apply Settings to
                                  All Components
```

## Mode-Specific Data Flows

### Standard Mode
```
User Request → UI Controller → Verse Manager → Display Verse
     ↓                             ↑
Copy/Share Request → Process → Return Formatted Verse
```

### Simulation Mode
```
Start Simulation → Simulation Controller → Simulated Feed Generator
        ↓                    ↓                      ↓
    Timer Events → Process Next Step → Verse Manager → API Service
        ↓                    ↓                      ↓
Visual Indicators → Update UI → Display Simulated Actions
```

### Advanced Developer Mode
```
Start Execution → Sandbox Controller → Automated Scrolling Engine
        ↓                 ↓                     ↓
    Timer Events → Process Next Post → Verse Manager → API Service
        ↓                 ↓                     ↓
Commenting Engine → Execute Comment → Update Statistics
        ↓
    Log Events
```

## Component Interactions

### API Service Interactions
- Communicates with AlQuran.cloud API
- Handles HTTP requests and responses
- Processes API data into usable format
- Manages error handling for API calls
- Provides data to Verse Manager

### Verse Manager Interactions
- Requests data from API Service
- Formats verses for display
- Caches verses to minimize API calls
- Provides verses to UI components
- Handles verse selection logic

### UI Controller Interactions
- Manages user input and events
- Coordinates between components
- Handles mode switching
- Updates UI based on application state
- Communicates with Configuration Manager

### Configuration Manager Interactions
- Stores user preferences
- Provides settings to all components
- Handles persistence between sessions
- Manages access controls for advanced mode
- Validates configuration changes

## Data Structures

### Verse Object
```json
{
  "number": 262,
  "surah": {
    "number": 2,
    "name": "Al-Baqarah",
    "englishName": "The Cow"
  },
  "text": {
    "arabic": "Arabic text of the verse",
    "translation": "English translation of the verse"
  },
  "audio": {
    "url": "URL to audio recitation"
  },
  "reference": "2:255"
}
```

### Configuration Object
```json
{
  "language": "en",
  "translation": "en.asad",
  "theme": "light",
  "fontSize": "medium",
  "simulationSpeed": 1.0,
  "advancedModeEnabled": false,
  "commentDelay": 10,
  "autoScrollDelay": 5
}
```

### Simulation State Object
```json
{
  "running": false,
  "currentStep": "scrolling",
  "currentPost": 2,
  "nextAction": "fetch_verse",
  "elapsedTime": 45,
  "posts": [
    { "id": 1, "content": "Post content...", "commented": true },
    { "id": 2, "content": "Post content...", "commented": false },
    { "id": 3, "content": "Post content...", "commented": false }
  ]
}
```
