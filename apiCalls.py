import json
import os

from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# System and user prompts
sysPrompt = """You are a history guide designed to output JSON. of format {
  "Place": "String",
  "Location": {
    "Country": "String",
    "Coordinates": {
      "Latitude": "String",
      "Longitude": "String"
    }
  },
  "History": "String... detailed story-like history, around 20 lines",
  "Ecological Relevance": "String",
  "Cultural Significance": "String",
  "Key Figures": [
    {
      "Name": "String",
      "Role": "String",
      "Contribution": "String"
    }... 3-5 key figures
  ],
  "Economic Importance": "String",
  "Major Landmarks": [
    {
      "Name": "String",
      "Description": "String"
    }... 3-5 major landmarks
  ],
  "Timeline": [
    {
      "Year": "String",
      "Details": "String"
    }... 10 major events, each with a detailed description
  ]
}
Ensure the history is rich in detail, weaving together significant events, cultural developments, and key figures in a narrative form. The timeline should highlight crucial moments, explaining their importance in shaping the place's history."""

userPrompt = f"Tell me about the history of: ."

# Function to call GPT-3 and retrieve historical data
def callGPT3(systemPrompt=sysPrompt, userPrompt=userPrompt, loc="", dataSave = False):
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": userPrompt + loc},
        ]
    )

    content_str = response.choices[0].message.content
    content_dict = json.loads(content_str)

    # Print content
    print(content_str)

    # Save response as text
    with open('response.txt', 'w') as f:
        f.write(content_str)

    if dataSave == True:
        os.makedirs('./data', exist_ok=True)
        place_name = content_dict.get("Place", "unknown").replace(" ", "_").lower()
        json_path = os.path.join('./data', f'{place_name}.json')
    else:
        place_name = content_dict.get("Place", "unknown").replace(" ", "_").lower()
        json_path = os.path.join('response.json') 
    
    with open(json_path, 'w') as f:
        json.dump(content_dict, f, indent=4)
    
    print(f"Data saved to {json_path}")
    return content_str

# Main execution
if __name__ == "__main__":
    
    
    # Example location to query
    
    popular_places = [
    "Hawa Mahal",
    "Twin towers",
    "Statue of liberty"
]
    
    # Call the function to retrieve data from GPT-3
    for location in popular_places:
        data = callGPT3(loc=location, dataSave=True)
    
    