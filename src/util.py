from geopy.geocoders import Nominatim
import os
import json

def reverse_geocode(latitude, longitude):
    geolocator = Nominatim(user_agent="weather_dashboard")
    location = geolocator.reverse((latitude, longitude))

    if location is not None:
        address = location.raw["address"]
        city = address.get("city", "")
        if not city:
            city = address.get("town", "")
        if not city:
            city = address.get("village", "")
        if not city:
            city = address.get("county", "")
        country = address.get("country", "")

        return {
            "city": city,
            "country": country
        }

def get_app_data():
    if os.path.exists("app_data.json"):
        with open("app_data.json", "r") as file:
            data = json.load(file)
            client_id = data.get("client_id")
            client_secret = data.get("client_secret")
            redirect_ui = data.get("redirect_ui")
            return client_id, client_secret, redirect_ui
    else:
        print("app_data.json file is missing!")
