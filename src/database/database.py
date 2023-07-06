import datetime
import os.path as path
from sqlalchemy import Column, Integer, Float, DateTime, create_engine, MetaData
from sqlalchemy.orm import relationship, Session, DeclarativeBase
from src.settings import PROJECT_PATH


class Base(DeclarativeBase):
    pass


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())
    indoor_temperature = Column(Float)
    indoor_humidity = Column(Integer)
    outdoor_temperature = Column(Float)
    outdoor_humidity = Column(Integer)
    co2 = Column(Integer)
    noise = Column(Integer)
    pressure = Column(Float)
    wind_strength = Column(Float)
    wind_angle = Column(Integer)
    gust_strength = Column(Float)
    gust_angle = Column(Integer)
    max_wind_strength = Column(Float)
    max_wind_angle = Column(Integer)
    date_max_wind_strength = Column(Integer)
    rain = Column(Float)
    sum_rain_1 = Column(Float)
    sum_rain_24 = Column(Float)

    def __init__(self, data):
        modules = data['body']['devices'][0]['modules']
        main_module_data = data['body']['devices'][0]['dashboard_data']

        # Dictionary mapping module types to their corresponding data fields
        module_data_map = {
            'NAModule1': {
                'outdoor_temperature': 'Temperature',
                'outdoor_humidity': 'Humidity'
            },
            'NAModule2': {
                'wind_strength': 'WindStrength',
                'wind_angle': 'WindAngle',
                'gust_strength': 'GustStrength',
                'gust_angle': 'GustAngle',
                'max_wind_strength': 'max_wind_str',
                'max_wind_angle': 'max_wind_angle',
                'date_max_wind_strength': 'date_max_wind_str'
            },
            'NAModule3': {
                'rain': 'Rain',
                'sum_rain_1': 'sum_rain_1',
                'sum_rain_24': 'sum_rain_24'
            }
        }

        main_module_data_map = {
            'indoor_temperature': 'Temperature',
            'indoor_humidity': 'Humidity',
            'co2': 'CO2',
            'noise': 'Noise',
            'pressure': 'Pressure'
        }

        # Process main module data
        for attr, field in main_module_data_map.items():
            setattr(self, attr, main_module_data.get(field))

        # Process other modules data
        for module in modules:
            module_type = module['type']
            if module_type in module_data_map:
                module_data = module['dashboard_data']
                data_fields = module_data_map[module_type]

                # Assign data to corresponding attributes
                for attr, field in data_fields.items():
                    setattr(self, attr, module_data.get(field))

    def __repr__(self):
        return f"Weather report from {self.timestamp}"


class DbManager:
    session = None

    @classmethod
    def initialize(cls):
        db_path = path.join(PROJECT_PATH, "db.sqlite")
        engine = create_engine(f"sqlite:///{db_path}", echo=True)
        cls.session = Session(engine)
        Base.metadata.create_all(engine)

    @classmethod
    def add_weather(cls, weather):
        cls.session.add(weather)
        cls.session.commit()

