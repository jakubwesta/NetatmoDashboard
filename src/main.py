from database.database import DbManager, Weather
from api.api_integration import User


def main():
    initialize()
    #data = get_station_data(ACCESS_TOKEN)
    #DbManager.add_weather(Weather(data))


# Checks if all necessary files exists
def initialize():
    DbManager.initialize()
    user = User.load()
    print(user.access_token)
    print(user.refresh_token)
    print(user.authenticated)


if __name__ == "__main__":
    main()
