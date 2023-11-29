import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")
ID = os.getenv("ID")
ACCOUNTID = os.getenv("ACCOUNTID")
PUUID = os.getenv("PUUID")
SUMMONERNAME = os.getenv("SUMMONERNAME")
MATCHID="OC1_526803580"

url = f"https://oc1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{ID}"
headers = {"X-Riot-Token": API_KEY}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Request was successful
    data = response.json()
    print(data)

    # Save the response data to a JSON file
    with open('spectator.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

    print("Response data saved to response_data.json")
else:
    print(f"Request failed with status code {response.status_code}")
    print("Response content:", response.text)