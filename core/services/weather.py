import os
import requests
from typing import Tuple, Dict, Optional, Any

API_KEY = os.getenv("WEATHERAPI_COM_APIKEY")
API_BASE_URL = "http://api.weatherapi.com/v1"

def get_current_weather(city: str) -> Tuple[int, Optional[Dict[str, Any]]]:
    if (API_KEY is None):
        return 500, None

    parameters = { "key": API_KEY, "q": city }
    api_response: requests.Response = requests.get(url = API_BASE_URL + "/current.json", params = parameters)

    if not api_response.ok:
        return api_response.status_code, None

    json_data: Dict = api_response.json()

    return api_response.status_code, json_data

def get_weather_forecast(city: str) -> Tuple[int, Optional[Dict[str, Any]]]:
    if (API_KEY is None):
        return 500, None

    parameters = { "key": API_KEY, "q": city }
    api_response: requests.Response = requests.get(url = API_BASE_URL + "/forecast.json", params = parameters)

    if not api_response.ok:
        return api_response.status_code, None

    json_data: Dict = api_response.json()

    return api_response.status_code, json_data
