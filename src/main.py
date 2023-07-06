import sys
from settings import SRC_PATH
from PyQt6.QtWidgets import QApplication
from database.database import DbManager, Weather
from api.api_integration import User, get_station_data
from gui.dashboard import DashboardWindow


def main():
    initialize()
    #DbManager.add_weather(Weather(get_station_data(User.USER.access_token)))

    app = QApplication(sys.argv)

    window = DashboardWindow()
    window.show()

    app.exec()


def initialize():
    sys.path.append(SRC_PATH) # Adds project folder to path to allow imports for sub-folders

    DbManager.initialize()
    User.load()

    print(User.USER.access_token)
    print(User.USER.refresh_token)
    print(User.USER.is_authenticated)


if __name__ == "__main__":
    main()
