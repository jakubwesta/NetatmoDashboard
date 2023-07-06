import os.path as path
import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSizePolicy,
    QStyleOption,
    QStyle,
    QLabel,
    QLineEdit,
    QCompleter,
    QGridLayout
)

from src.settings import PROJECT_PATH
from src.stats import Stat

WINDOW_SIZE_X = 1400
WINDOW_SIZE_Y = 800

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather Dashboard")
        self.resize(WINDOW_SIZE_X, WINDOW_SIZE_Y)

        # todo
        #self.setMenuWidget(TitleBar(self))
        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Creates a central widget for whole window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # main_layout will be the whole central_widget, and will contain all other sub-layouts
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(SideMenu(), 15)
        main_layout.addWidget(MainWeatherMenu(), 50)
        main_layout.addWidget(SideWeatherMenu(), 25)


# Class for areas containing various elements, mostly QoL usage
class AreaWidget(QWidget):
    qss_path = path.join(path.dirname(path.abspath(__file__)), "qss")

    # name is a lowercase string that will be object name and a stylesheet file
    def __init__(self, name):
        super().__init__()
        self.setObjectName(name)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        with open(path.join(AreaWidget.qss_path, name + ".qss"), "r") as stylesheet_file:
            self.setStyleSheet(stylesheet_file.read())

    # Based on Qt docs, required for custom widgets to render properly, background won't load without it
    def paintEvent(self, event):
        qp = QPainter(self)
        opt = QStyleOption()
        opt.initFrom(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, qp, self)


class SideMenu(AreaWidget):
    def __init__(self):
        super().__init__("side_menu")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 10, 20, 10)
        self.setLayout(self.layout)
        self.setFixedWidth(250)

        self.layout.addWidget(QPushButton("Indoor"))
        self.layout.addWidget(QPushButton("Outdoor"))
        self.layout.addStretch(1)
        self.layout.addWidget(QPushButton("Settings"))
        self.layout.addWidget(QPushButton("Logout"))


class SideWeatherMenu(AreaWidget):
    def __init__(self):
        super().__init__("side_weather_menu")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)
        self.setFixedWidth(400)

        # Top part, Date, hour and station location
        top_box = QHBoxLayout()
        top_box.setAlignment(Qt.AlignmentFlag.AlignTop)
        date_hour_box = QVBoxLayout()
        hour_label = QLabel("18:27")
        date_label = QLabel("Thursday, July 6, 2023")
        date_hour_box.addWidget(hour_label)
        date_hour_box.addWidget(date_label)
        location_label = QLabel("Rumia")
        top_box.addLayout(date_hour_box)
        top_box.addWidget(location_label)

        # Middle part, modules battery levels
        modules_battery_label = QLabel("Modules battery")
        modules_battery_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        modules_battery_box = QVBoxLayout()
        modules_battery_box.setAlignment(Qt.AlignmentFlag.AlignTop)





        # Bottom part, sunrise and sunset
        sun_label = QLabel("Sunrise and sunset")
        sun_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        sun_box = QVBoxLayout()
        sun_box.setAlignment(Qt.AlignmentFlag.AlignTop)
        sunrise_button = StatButton(Stat.SUNRISE)
        sunset_button = StatButton(Stat.SUNSET)
        sun_box.addWidget(sunrise_button)
        sun_box.addWidget(sunset_button)

        self.layout.addLayout(top_box)
        self.layout.addWidget(modules_battery_label)
        self.layout.addLayout(modules_battery_box)
        self.layout.addWidget(sun_label)
        self.layout.addLayout(sun_box)




class MainWeatherMenu(AreaWidget):
    def __init__(self):
        super().__init__("main_weather_menu")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)
        self.setMinimumWidth(800)

        # Top bar, location, searching
        location_bar = QHBoxLayout()
        location_bar.setAlignment(Qt.AlignmentFlag.AlignTop)
        location_bar.setContentsMargins(5, 5, 5, 5)
        location_bar.setSpacing(2)

        # Current location, top left corner
        location_box = QVBoxLayout()
        city_label = QLabel("Rumia")
        country_label = QLabel("Poland")
        location_box.addWidget(city_label)
        location_box.addWidget(country_label)

        # Location searching, top middle
        location_search_box = QLineEdit()
        location_search_box.setPlaceholderText("Weather for other locations...")
        location_search_completer = QCompleter()
        location_search_completer.setModel(QStringListModel(["Rumia", "Gdynia", "Sopot", "Gdańsk"])) # todo
        location_search_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        location_search_box.setCompleter(location_search_completer)
        location_search_button = QPushButton("") # Searches location from search_box
        location_search_button.clicked.connect(self.location_search_button_action)
        location_home_button = QPushButton("") # Sets location to current home
        location_home_button.clicked.connect(self.location_home_button_action)

        # Adding made widgets to location bar
        location_bar.addLayout(location_box)
        location_bar.addWidget(location_search_box)
        location_bar.addWidget(location_search_button)
        location_bar.addWidget(location_home_button)


        # Current overview, middle section
        overview_label = QLabel("Current overview")
        overview_box = QGridLayout()
        overview_box.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Dict with overview buttons_name: (x, y) pos
        overview_items = {
            Stat.TEMPERATURE: (0, 0),
            Stat.CO2: (1, 0),
            Stat.NOISE: (0, 1),
            Stat.HUMIDITY: (1, 1)
        }

        # Adding button to overview
        for (key, value) in overview_items.items():
            overview_box.addWidget(StatButton(key), *value)


        # Plot with recent data at the bottom
        plot_label = QLabel("... plot")
        plot = StatPlot()

        self.layout.addLayout(location_bar)
        self.layout.addWidget(overview_label)
        self.layout.addLayout(overview_box)
        self.layout.addWidget(plot_label)
        self.layout.addWidget(plot)

    def location_search_button_action(self):
        pass

    def location_home_button_action(self):
        pass


class StatButton(QPushButton):
    # icon is an optional file name, in assets/icons/, for example rain.png
    def __init__(self, stat, icon=None):
        super().__init__()
        self.setObjectName(stat.label.lower())
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        if icon is not None:
            icon_label.setPixmap(QPixmap(path.join(PROJECT_PATH, "assets", "icons", icon)).scaled(16, 16))

        stat_box = QVBoxLayout()
        stat_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        stat_value_label = QLabel(stat.append_unit(21))  # todo
        stat_name_label = QLabel(stat.label)
        stat_box.addWidget(stat_value_label)
        stat_box.addWidget(stat_name_label)

        self.layout.addWidget(icon_label)
        self.layout.addLayout(stat_box)


class StatPlot(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        # Generate some sample data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        # Create the curve item
        curve = pg.PlotDataItem(x, y, pen='b')
        self.addItem(curve)





"""
class TitleBar(AreaWidget):
    def __init__(self, parent):
        super().__init__("title_bar.qss")
        self.setFixedHeight(30)
        self.parent = parent

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_label = QLabel("Weather Dashboard")
        self.title_label.setFixedHeight(35)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_size = 35

        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size, btn_size)
        self.btn_close.setStyleSheet("background-color: red;")

        self.btn_min = QPushButton("-")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet("background-color: gray;")

        self.btn_max = QPushButton("+")
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size, btn_size)
        self.btn_max.setStyleSheet("background-color: gray;")


        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)
        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(TitleBar, self).resizeEvent(QResizeEvent)
        self.title_label.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        self.parent.showMaximized()

    def btn_min_clicked(self):
        self.parent.showMinimized()


"""
