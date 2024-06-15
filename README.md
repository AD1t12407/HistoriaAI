# Location History Viewer

## Overview

The Location History Viewer is an AI-based solution designed to provide historical information and significant events related to a specific location. The system takes input from a camera and geolocation data, utilizes the Google Lens API for image detection, Google Maps/Google Earth API for geolocation, and OpenAI's GPT-4 or Wikipedia API for historical data. Additionally, it features voice output in multiple languages using Google Cloud's Text-to-Speech service.

## Project Structure

```
my_project/
├── app.py
├── camera.py
├── location.py
├── history.py
├── google_apis.py
├── requirements.txt
└── README.md
```

- **app.py**: The main Streamlit application file integrating all components.
- **camera.py**: Handles the video capture from the webcam.
- **location.py**: Retrieves geolocation data based on latitude and longitude.
- **history.py**: Fetches historical information from OpenAI GPT-4 and Wikipedia API.
- **google_apis.py**: Contains functions to interact with Google Lens API and Google Cloud Text-to-Speech API.
- **requirements.txt**: Lists all the required Python packages.
- **README.md**: Project documentation.

## Installation

### Prerequisites

- Python 3.7 or higher
- Google Cloud account with Vision and Text-to-Speech APIs enabled
- OpenAI API key

### Setup

1. **Clone the repository:**

`bash
   git clone https://github.com/yourusername/location-history-viewer.git
   cd location-history-viewer
   `

2. **Install the required libraries:**

`bash
   pip install -r requirements.txt
   `

3. **Set up Google Cloud credentials:**

Follow the [Google Cloud instructions](https://cloud.google.com/docs/authentication/getting-started) to set up authentication and download your `credentials.json` file. Set the environment variable:

`bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
   `

4. **Set up OpenAI API key:**

`bash
   export OPENAI_API_KEY="your-openai-api-key"
   `

## Usage

1. **Run the Streamlit app:**

`bash
   streamlit run app.py
   `

2. **Interacting with the app:**

- Enter the latitude and longitude in the sidebar to get the location data.
   - Click "Get Location Data" to retrieve and display historical information.
   - Use the "Camera Feed" section to view the live video feed from your webcam.
   - Click "Detect Content" to use Google Lens API for object detection in the video feed.
   - Click "Read History" to listen to the historical information in the selected language.

## Features

- **Camera Input:** Captures video feed from the webcam.
- **Geolocation Retrieval:** Fetches location data based on latitude and longitude.
- **Historical Information:** Retrieves history and significant events using OpenAI GPT-4 or Wikipedia API.
- **Object Detection:** Uses Google Lens API to detect objects in the camera feed.
- **Voice Output:** Converts text to speech using Google Cloud Text-to-Speech API in multiple languages.

##--------------------------------------------##
Street view- map embedding?

## Project Files

### `app.py`

The main application file that integrates the camera feed, geolocation retrieval, historical data fetching, and text-to-speech functionalities into a Streamlit app.

### `camera.py`

Handles video capture from the webcam using OpenCV.

### `location.py`

Retrieves geolocation data based on provided latitude and longitude using the Geopy library.

### `history.py`

Fetches historical information using OpenAI GPT-4 and Wikipedia API.

### `google_apis.py`

Contains functions to interact with Google Lens API for object detection and Google Cloud Text-to-Speech API for voice output.

### `requirements.txt`

Lists all the required Python packages for the project:

```
streamlit
opencv-python
geopy
requests
google-cloud-vision
google-cloud-texttospeech
openai
```
# HistoriaAI
