import requests

from app_configs import *
from class_Tweet import Response

# API URL
def responseOb():
    url =SIMS_API_SOURCE_BASEURL + SIMS_API_SOURCE_ENDPOINT

    # Query Parameters
    params = PARAMS

    # Headers
    headers = HEADERS

    # Make the GET request
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        
        # Print the JSON response
        print(response.json())

        # Convert JSON string to Python dictionary
        data_dict = response.json()

        # Convert dictionary to Python object
        responseOb = Response(**data_dict)

        # print(responseOb.data.device_name)  # Output: Emon
        # print(responseOb.data.fb_user.name)  # Output: Aleya
        # print(responseOb.data.sources[0].title)  # Output: JamunaTV

        return responseOb

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    

    # Accessing the data
    