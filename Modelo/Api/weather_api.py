import requests

API_KEY = "72acfa86a8a442dba1c183023262307"

BASE_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather(lat, lon):

    response = requests.get(
        BASE_URL,
        params={
            "key": API_KEY,
            "q": f"{lat},{lon}"
        }
    )

    data = response.json()

    return {
        "rain": data["current"]["precip_mm"],
        "visibility": data["current"]["vis_km"] * 1000,
        "wind_speed": data["current"]["wind_kph"]
    }