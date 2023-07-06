import os.path as path
from PyQt6.QtCore import QSize, Qt, QPoint, QStringListModel
from PyQt6.QtGui import QPalette, QColor, QPainter
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSizePolicy,
    QStyleOption,
    QStyle, QLayout, QLabel, QLineEdit, QCompleter, QGridLayout
)
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

    def __init__(self, stylesheet):
        super().__init__()
        with open(path.join(AreaWidget.qss_path, stylesheet), "r") as stylesheet_file:
            self.setStyleSheet(stylesheet_file.read())
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # Based on Qt docs, required for custom widgets to render properly, background won't load without it
    def paintEvent(self, event):
        qp = QPainter(self)
        opt = QStyleOption()
        opt.initFrom(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, qp, self)


class SideMenu(AreaWidget):
    def __init__(self):
        super().__init__("side_menu.qss")
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
        super().__init__("side_weather_menu.qss")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setFixedWidth(400)


class MainWeatherMenu(AreaWidget):
    def __init__(self):
        super().__init__("main_weather_menu.qss")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setMinimumWidth(800)

        # Top bar, location, searching
        location_bar = QHBoxLayout()
        location_bar.setAlignment(Qt.AlignmentFlag.AlignTop)
        location_bar.setContentsMargins(5, 5, 5, 5)
        location_bar.setSpacing(2)
        location_bar_widget = QWidget()
        location_bar_widget.setObjectName("location")
        location_bar_widget.setLayout(location_bar)

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


        self.layout.addWidget(location_bar_widget)
        self.layout.addWidget(overview_label)
        self.layout.addLayout(overview_box)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def location_search_button_action(self):
        pass

    def location_home_button_action(self):
        pass


class StatButton(QPushButton):
    def __init__(self, stat):
        super().__init__()
        self.setObjectName(stat.label.lower())
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        stat_box = QVBoxLayout()
        stat_value_label = QLabel(stat.append_unit(21)) # todo
        stat_name_label = QLabel(stat.label)
        stat_box.addWidget(stat_value_label)
        stat_box.addWidget(stat_name_label)

        self.layout.addLayout(stat_box)


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
