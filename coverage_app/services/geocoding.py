import requests
from django.conf import settings
from typing import Dict, Any


class GeocodingError(Exception):
    pass


def get_geocoding_data(address: str) -> Dict[str, Any]:
    params = {"q": address, "limit": 1}
    response = requests.get(settings.GEOCODING_API_URL, params=params)

    if response.status_code != 200:
        raise GeocodingError("Error calling geocoding API.")

    data = response.json()
    if not data["features"]:
        raise GeocodingError("Address not found.")

    return data["features"][0]


def reverse_geocode_city(longitude: float, latitude: float) -> str:
    params = {"lon": longitude, "lat": latitude}
    response = requests.get(settings.REVERSE_GEOCODING_API_URL, params=params)

    if response.status_code != 200:
        raise GeocodingError("Error calling reverse geocoding API.")

    data = response.json()
    if data["features"]:
        return data["features"][0]["properties"].get("city", "")
    return ""


def get_user_location(address: str) -> Dict[str, Any]:
    geocoding_data = get_geocoding_data(address)
    return {
        "city": geocoding_data["properties"]["city"],
        "longitude": geocoding_data["geometry"]["coordinates"][0],
        "latitude": geocoding_data["geometry"]["coordinates"][1],
    }
