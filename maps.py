import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
# Function to get autocomplete suggestions using Google Places API
def get_autocomplete_results(input_text):
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={input_text}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    return response.json()

# Function to get place details using Google Places API
def get_place_details(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_address,name,geometry&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    return response.json()

# Function to get Street View URL
def get_street_view_url(lat, lon):
    return f"https://www.google.com/maps/embed/v1/streetview?key={GOOGLE_MAPS_API_KEY}&location={lat},{lon}&heading=210&pitch=10&fov=35"

# Function to get Map URL
def get_map_url(lat, lon):
    return f"https://www.google.com/maps/embed/v1/view?key={GOOGLE_MAPS_API_KEY}&center={lat},{lon}&zoom=14&maptype=satellite"

def image(autocomplete_results):
    place_predictions = [result['description'] for result in autocomplete_results['predictions']]
    selected_place = st.selectbox("Select a place", place_predictions)
    
    if selected_place:
        place_id = [result['place_id'] for result in autocomplete_results['predictions'] if result['description'] == selected_place][0]
        place_details = get_place_details(place_id)
        
        if place_details['status'] == 'OK':
            lat = place_details['result']['geometry']['location']['lat']
            lon = place_details['result']['geometry']['location']['lng']

            st.write(f"Selected Location: {place_details['result']['name']} ({lat}, {lon})")

            # Step 2: Show Street View
            street_view_url = get_street_view_url(lat, lon)
            st.markdown(f'<iframe width="700" height="400" frameborder="0" style="border:0" src="{street_view_url}" allowfullscreen></iframe>', unsafe_allow_html=True)

            # Step 3: Show Embedded Map
            map_url = get_map_url(lat, lon)
            st.markdown(f'<iframe width="700" height="400" frameborder="0" style="border:0" src="{map_url}" allowfullscreen></iframe>', unsafe_allow_html=True)


        else:
            st.error("Place details not found.")

def main():
    st.title("Location History Viewer")

    # User input for location autocomplete
    input_text = st.text_input("Enter a location", "")
    
    if input_text:
        autocomplete_results = get_autocomplete_results(input_text)
        
        if autocomplete_results['status'] == 'OK':
            place_predictions = [result['description'] for result in autocomplete_results['predictions']]
            selected_place = st.selectbox("Select a place", place_predictions)
            
            if selected_place:
                place_id = [result['place_id'] for result in autocomplete_results['predictions'] if result['description'] == selected_place][0]
                place_details = get_place_details(place_id)
                
                if place_details['status'] == 'OK':
                    lat = place_details['result']['geometry']['location']['lat']
                    lon = place_details['result']['geometry']['location']['lng']

                    st.write(f"Selected Location: {place_details['result']['name']} ({lat}, {lon})")

                    # Step 2: Show Street View
                    street_view_url = get_street_view_url(lat, lon)
                    st.markdown(f'<iframe width="700" height="400" frameborder="0" style="border:0" src="{street_view_url}" allowfullscreen></iframe>', unsafe_allow_html=True)

                    # Step 3: Show Embedded Map
                    map_url = get_map_url(lat, lon)
                    st.markdown(f'<iframe width="700" height="400" frameborder="0" style="border:0" src="{map_url}" allowfullscreen></iframe>', unsafe_allow_html=True)

                    # Additional feature: Show Timelapse (mock example)
                    st.subheader("Timelapse through the years:")
                    years = [2000, 2005, 2010, 2015, 2020]
                    for year in years:
                        st.image(f"https://via.placeholder.com/600x400.png?text=Timelapse+{year}", caption=f"Year {year}")

                else:
                    st.error("Place details not found.")
            
        else:
            st.error("Autocomplete failed. Please try again.")

if __name__ == "__main__":
    main()