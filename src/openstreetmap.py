import logging
import requests

def get_coordinates(location_name:str) -> tuple[float, float]:
    """
    Retrieves latitude and longitude coordinates for a given location name from OpenStreetMap.

    Args:
        location_name (str): Name of the location (e.g., city, landmark).

    Returns:
        tuple: (latitude, longitude) coordinates.
    """
    data = _get_data(location_name)
    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return (lat, lon)
    else:
        return None
    

def _get_data(location_name : str) -> dict:
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1,  # Limit to one result
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            logging.warn(f"Received unexpected status code for '{location_name}'. {response.status_code}: {response.text}")

        data = response.json()

        if data:
            return data
        else:
            logging.warn(f"No results found for '{location_name}'")
            return None

    except requests.RequestException as e:
        logging.warn(f"Error fetching data: {e}")
        return None