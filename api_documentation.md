# AlQuran.Cloud API Documentation

## Base URL
```
http://api.alquran.cloud/v1
```

## Key Endpoints

### 1. Get a Specific Ayah (Verse)
Retrieves a specific verse by number (1-6236) or surah:ayah reference.

**Endpoint:** `/ayah/{reference}`

**Parameters:**
- `reference`: Ayah number (1-6236) or surah:ayah format (e.g., 2:255)

**Example Requests:**
- `http://api.alquran.cloud/v1/ayah/262` - Get verse 262
- `http://api.alquran.cloud/v1/ayah/2:255` - Get Surah 2, Verse 255

### 2. Get a Specific Ayah with Translation
Retrieves a specific verse with translation in the specified edition.

**Endpoint:** `/ayah/{reference}/{edition}`

**Parameters:**
- `reference`: Ayah number (1-6236) or surah:ayah format
- `edition`: Edition identifier (e.g., en.asad for Muhammad Asad's English translation)

**Example Requests:**
- `http://api.alquran.cloud/v1/ayah/262/en.asad` - Get verse 262 with Asad's English translation
- `http://api.alquran.cloud/v1/ayah/2:255/en.asad` - Get Surah 2, Verse 255 with Asad's English translation

### 3. Get a Specific Ayah with Audio
Retrieves a specific verse with audio recitation.

**Endpoint:** `/ayah/{reference}/{edition}`

**Parameters:**
- `reference`: Ayah number (1-6236) or surah:ayah format
- `edition`: Audio edition identifier (e.g., ar.alafasy for Mishary Alafasy's recitation)

**Example Request:**
- `http://api.alquran.cloud/v1/ayah/262/ar.alafasy` - Get verse 262 with Alafasy's recitation

### 4. Get a Specific Ayah with Multiple Editions
Retrieves a specific verse with multiple editions (translations and/or audio).

**Endpoint:** `/ayah/{reference}/editions/{editions}`

**Parameters:**
- `reference`: Ayah number (1-6236) or surah:ayah format
- `editions`: Comma-separated list of edition identifiers

**Example Request:**
- `http://api.alquran.cloud/v1/ayah/262/editions/quran-uthmani,en.asad,en.pickthall` - Get verse 262 in Arabic with two English translations

### 5. Get Available Editions
Retrieves a list of all available text and audio editions.

**Endpoint:** `/edition`

**Example Request:**
- `http://api.alquran.cloud/v1/edition`

### 6. Get Meta Data
Retrieves metadata about Surahs, Pages, Hizbs, and Juzs.

**Endpoint:** `/meta`

**Example Request:**
- `http://api.alquran.cloud/v1/meta`

## Response Format
All API responses are in JSON format with the following structure:

```json
{
  "code": 200,
  "status": "OK",
  "data": {
    // Response data specific to the endpoint
  }
}
```

## Random Verse Implementation
The API does not have a dedicated random verse endpoint, but random verses can be retrieved by generating a random number between 1 and 6236 (total number of verses in the Quran) and using it with the ayah endpoint.

**Example Implementation in JavaScript:**
```javascript
function getRandomVerse() {
  const randomAyahNumber = Math.floor(Math.random() * 6236) + 1;
  return fetch(`http://api.alquran.cloud/v1/ayah/${randomAyahNumber}/editions/quran-uthmani,en.asad`)
    .then(response => response.json())
    .then(data => data.data);
}
```

**Example Implementation in Python:**
```python
import random
import requests

def get_random_verse():
    random_ayah_number = random.randint(1, 6236)
    response = requests.get(f"http://api.alquran.cloud/v1/ayah/{random_ayah_number}/editions/quran-uthmani,en.asad")
    return response.json()["data"]
```

## Notes
- The API is free to use and does not require authentication
- All endpoints support CORS for cross-domain requests
- The API returns HTTP 200 for successful requests and appropriate error codes for failures
