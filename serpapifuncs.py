import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SERP_API_KEY")
url = "https://serpapi.com/search.json"
search_string = input("Enter search query: ")

# Prepare parameters to send to SerpAPI
payload = {
    "engine": "amazon",
    "k": search_string,
    "amazon_domain": "amazon.in",
    "api_key": api_key,
    "page": 1
}

# Make the GET request to the SerpAPI
req = requests.get(url, params=payload)

if req.status_code == 200:
    data = req.json()
    for i in range(len(data['organic_results'])):
        #print(json.dumps(data['organic_results'][i], indent=2))
        print(data['organic_results'][i]['title'])
        print(data['organic_results'][i]['link_clean'])
        print(data['organic_results'][i]['thumbnail'])
        print(f"Price: {data['organic_results'][i]['extracted_price']}")
        print(f"Old Price: {data['organic_results'][i]['extracted_old_price']}")
        print()


else:
    print(f"Error: {req.status_code}")