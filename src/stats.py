from enum import Enum


class Stat(Enum):
    TEMPERATURE = "°C"
    CO2 = "ppm"
    NOISE = "dB"
    HUMIDITY = "%"
    PRESSURE = "hPa"
    RAIN = "mm"
    WIND = "km/h"

    def append_unit(self, value):
        return str(value) + " " + self.unit

    @classmethod
    def unit_for_label(cls, label):
        for member in cls:
            if member.label == label:
                return member.unit
        return None

    @property
    def label(self):
        return self.name.lower().capitalize()

    @property
    def unit(self):
        return self.value
