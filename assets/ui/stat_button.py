from PyQt6 import QtCore, QtGui, QtWidgets
import os
from PyQt6.QtCore import QPropertyAnimation, QVariantAnimation, QEasingCurve
from PyQt6.QtGui import QColor


class StatButton(QtWidgets.QPushButton):
    def __init__(self, name: str, value: str, parent=None):
        super().__init__(parent)
        self.name = name
        self.value = value
        self.nameLabel = QtWidgets.QLabel(self)
        self.valueLabel = QtWidgets.QLabel(self)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.setupUi()

    def setupUi(self):
        self.setMinimumSize(200, 300)
        self.setSizeIncrement(2, 3)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.verticalLayout.setObjectName("verticalLayout")

        font = QtGui.QFont()
        font.setPointSize(30)
        self.valueLabel.setText(self.value)
        self.valueLabel.setFont(font)
        self.valueLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.valueLabel)

        font = QtGui.QFont()
        font.setPointSize(15)
        self.nameLabel.setText(self.name)
        self.nameLabel.setFont(font)
        self.nameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.nameLabel)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        script_directory = os.path.dirname(os.path.abspath(__file__))
        style_file = os.path.join(script_directory, "../../src/widgets/stat_button.qss")
        with open(style_file, "r") as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)


