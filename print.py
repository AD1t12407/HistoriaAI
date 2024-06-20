import streamlit as st
import json

# Function to read JSON data from the specified path
def read_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error reading JSON file: {e}")
        return None

# Function to display the JSON data in Streamlit
def display_data(data):
    if data:
        st.header(data.get("Place", "Unknown Place"))
        
        st.subheader("Location")
        location = data.get("Location", {})
        st.write(f"Country: {location.get('Country', 'Unknown')}")
        coordinates = location.get("Coordinates", {})
        st.write(f"Coordinates: Latitude {coordinates.get('Latitude', 'Unknown')}, Longitude {coordinates.get('Longitude', 'Unknown')}")
        
        st.subheader("History")
        st.write(data.get("History", "No history available."))
        
        st.subheader("Ecological Relevance")
        st.write(data.get("Ecological Relevance", "No ecological relevance available."))
        
        st.subheader("Cultural Significance")
        st.write(data.get("Cultural Significance", "No cultural significance available."))
        
        st.subheader("Key Figures")
        key_figures = data.get("Key Figures", [])
        if key_figures:
            for figure in key_figures:
                st.write(f"**{figure.get('Name', 'Unknown')}** - {figure.get('Role', 'Unknown')}")
                st.write(f"Contribution: {figure.get('Contribution', 'No contribution details available.')}")
        else:
            st.write("No key figures available.")
        
        st.subheader("Economic Importance")
        st.write(data.get("Economic Importance", "No economic importance available."))
        
        st.subheader("Major Landmarks")
        landmarks = data.get("Major Landmarks", [])
        if landmarks:
            for landmark in landmarks:
                st.write(f"**{landmark.get('Name', 'Unknown')}**")
                st.write(f"{landmark.get('Description', 'No description available.')}")
        else:
            st.write("No major landmarks available.")
        
        st.subheader("Timeline of Major Events")
        timeline = data.get("Timeline", [])
        if timeline:
            for event in timeline:
                st.write(f"**{event.get('Year', 'Unknown Year')}**: {event.get('Details', 'No details available.')}")
        else:
            st.write("No major events available.")
    else:
        st.write("No data to display.")

# Streamlit application
def main():
    st.title('Historical Data Viewer')

    data = read_json("./data/whitehouse.json")
    display_data(data)
   
if __name__ == "__main__":
    main()
