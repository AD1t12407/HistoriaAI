import streamlit as st
import base64
import requests
from dotenv import load_dotenv
from apiCalls import callGPT3
from maps import get_autocomplete_results, image
from google.cloud import texttospeech
from print import read_json, display_data
from voice import audio
import os

# Load environment variables
load_dotenv()

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")



# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_supported_languages():
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices()
    languages = set()
    for voice in response.voices:
        for language_code in voice.language_codes:
            languages.add(language_code)
    return sorted(list(languages))

def main():
    st.title("HISTORAI")
    st.write("Welcome to Historai! Your AI-powered History companion.")
    st.write("Previous users have explored places like ..")
    
    # Image from a local file
    local_image_path = "./assets/historai.jpg"
    st.image(local_image_path, caption="Local Image", use_column_width=True)
    
    # Option to either upload an image or enter a location manually
    option = st.radio("Choose an option", ("Upload Image", "Enter Location Manually"))
    
    input_landmark = None  # Initialize input_landmark with None

    if option == "Upload Image":
        # Upload an image
        uploaded_file = st.file_uploader("Upload a picture", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Save the uploaded image locally
            with open(local_image_path, "wb") as f:
                f.write(uploaded_file.read())
            
            # Get base64 encoding of the uploaded image
            base64_image = encode_image(local_image_path)

            # Prompt for the historian to guess the name and location
            prompt = "You are a historian. Guess the name of the location in one word."

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 20
            }

            # Send request to OpenAI API
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            # Display response from API
            if response.status_code == 200:
                json_response = response.json()
                if 'choices' in json_response and len(json_response['choices']) > 0:
                    input_landmark = json_response['choices'][0]['message']['content']
                    st.write(f"Generated Location Name: {input_landmark}")
                else:
                    st.write("No valid response found.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")

    elif option == "Enter Location Manually":
        # Manually enter a location
        input_landmark = st.text_input("Enter a location", "VNR VJIET")

    # Ensure input_landmark is not None before using it
    if input_landmark is not None:
        autocomplete_results = get_autocomplete_results(input_landmark)
        
        if autocomplete_results['status'] == 'OK':   
            image(autocomplete_results=autocomplete_results)
            st.write("Images render")
        else:
            st.error("Autocomplete failed. Please try again.")

        # Location textbox
        user_input = autocomplete_results["predictions"][0]["description"]
        st.write(user_input)

        if st.button('Submit'):
            # Call API function (example: callGPT3)
            res = callGPT3(loc=user_input)
            print(res)  # Print or process response as needed
            data = read_json("./response.json")
            display_data(data)

        # Text-to-Speech functionality
        data = read_json("./response.json")
        history = data.get("History", "No history available.")
        ecological = data.get("Ecological Relevance", "No ecological relevance available.")
        
        if st.button("Convert to Speech", key="convert_speech_button"):


            if history:
                with st.spinner("Generating speech..."):
                    languages = get_supported_languages()
                    
                    language = st.selectbox("Select Language:", languages)
                    gender = st.selectbox("Select Voice Gender:", ["Neutral", "Male", "Female"])

                    gender_map = {
                        "Neutral": texttospeech.SsmlVoiceGender.NEUTRAL,
                        "Male": texttospeech.SsmlVoiceGender.MALE,
                        "Female": texttospeech.SsmlVoiceGender.FEMALE,
                    }
                    audio_content = audio(history,language,gender_map[gender])
                    st.audio(audio_content, format="audio/mp3")
            else:
                st.error("No text to convert to speech.")

if __name__ == "__main__":
    main()
