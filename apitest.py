from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
from datetime import datetime
import pytz
import requests
from selenium.webdriver.chrome.options import Options

import requests

# Define the API URL
api_url = "http://192.168.200.94:8051/create/scraped-data?platform=X"

try:
    # Send a GET request
    response = requests.get(api_url)

    # Check the status code
    if response.status_code == 200:
        print("API is working!")
        print("Response:", response.json())  # Assuming the API returns JSON
    else:
        print(f"API returned an error. Status Code: {response.status_code}")
        print("Response:", response.text)  # Print the response for debugging

except requests.exceptions.RequestException as e:
    print("Error while connecting to the API:", e)


with open("সংস্কার.json", "r",encoding="utf-8", errors="ignore") as file:
        # Load the JSON data
        data = json.load(file)

for d in  data:
    print(type(d))

    json_data = json.dumps(d)

    print(type(json_data))

    res = requests.post('http://192.168.200.94:8051/create/scraped-data?platform=X',json_data)
    print(res.status_code)
    if res.status_code == 200 :
        print(res)
        print("success")
    else :
        print("Post Fail")
