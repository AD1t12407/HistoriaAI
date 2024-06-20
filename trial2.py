import streamlit as st
import base64
import requests

# OpenAI API Key
api_key = ""

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def main():
    st.title("HISTORAI")
    st.write("Welcome to HistorAI, a platform that helps you identify historical figures from images.Users previously explored places such as:")
    # Display local image
    local_image_path = "./historai.jpg"
    st.image(local_image_path, caption="Local Image", use_column_width=True)

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
                generated_landmark = json_response['choices'][0]['message']['content']
                st.write(f"Generated Location Name: {generated_landmark}")
            else:
                st.write("No valid response found.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()
