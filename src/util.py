from geopy.geocoders import Nominatim

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
