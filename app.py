# app.py
import streamlit as st
from apiCalls import callGPT3
from dotenv import load_dotenv
from maps import get_autocomplete_results, get_map_url, get_place_details, get_street_view_url, image
from print import read_json, display_data
from voice import synthesize_text


load_dotenv()

def main():
    st.title("HISTORAI")
    # Image from a local file
    local_image_path = "historai.jpg"
    st.image(local_image_path, caption="Local Image", use_column_width=True)
    
    # access the camera and takes a picture 
    #picture = st.camera_input("Take a picture")

    #if picture:
        #rtimage=st.image(picture)
        #st.write(rtimage)

    input_landmark = st.text_input("Enter a location", "VNR VJIET")
    
    if input_landmark:
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
        res = callGPT3(loc=user_input)
        print(res)
        data = read_json("./response.json")
        display_data(data)
    
    # Text-to-Speech
    # read the JSON data from the response.json file
    data = read_json("./response.json")
    history =   data.get("History", "No history available.")
    ecological = data.get("Ecological Relevance", "No ecological relevance available.")
    
    # Synthesize the text to speech
    if st.button("Convert to Speech"):
        if history:
            with st.spinner("Generating speech..."):
                audio_content = synthesize_text(history)
                st.audio(audio_content, format="audio/mp3")
        else:
            st.error("No text to convert to speech.")
    
    
    

if __name__ == "__main__":
    main()
