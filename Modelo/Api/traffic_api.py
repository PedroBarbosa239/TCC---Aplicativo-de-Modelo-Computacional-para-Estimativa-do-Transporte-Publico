import requests

API_KEY = "eUQPtcujB8URBhJGsvRro880XWK2OTCi"

BASE_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"


def get_traffic(lat, lon):

    params = {
        "point": f"{lat},{lon}",
        "key": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()["flowSegmentData"]

    congestion = (
        100
        - (data["currentSpeed"] /
           data["freeFlowSpeed"]) * 100
    )

    return {
        "current_speed": data["currentSpeed"],
        "free_speed": data["freeFlowSpeed"],
        "congestion": congestion
    }