import os
import requests
from typing import Tuple, Dict, Optional, Any

def get_current_weather(city: str) -> Tuple[int, Optional[Dict[str, Any]]]:
    API_KEY = os.getenv("WEATHERAPI_COM_APIKEY")

    if (API_KEY is None):
        return 500, None

    API_BASE_URL = "http://api.weatherapi.com/v1"

    parameters = { "key": API_KEY, "q": city }
    api_response: requests.Response = requests.get(url = API_BASE_URL + "/current.json", params = parameters)

    if not api_response.ok:
        return api_response.status_code, None

    json_data: Dict = api_response.json()

    return api_response.status_code, json_data
