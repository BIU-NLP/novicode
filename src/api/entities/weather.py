from __future__ import annotations
from entities.entity import Entity
from entities.resolvable import Resolvable


class WeatherAttribute(Entity, Resolvable):
    """
    The WeatherAttribute entity class is used to represent an attribute of the weather.
    An attribute of the weather can be a weather condition (e.g., rain, sunny, cold, etc.).
    This class inherits from the Entity class and the Resolvable class.
    """

    pass


class WeatherTemperature(Entity, Resolvable):
    """
    The WeatherTemperature entity class is used to represent a temperature of the weather.
    A temperature of the weather can be a specific temperature, a range of temperatute, or a
    description of temperature (e.g., less than 80 degrees).
    This class inherits from the Entity class and the Resolvable class.
    """

    pass


class WeatherForecastEntity(Entity):
    """
    The WeatherForecastEntity class is used to represent a weather forecast. The find_weather_forecasts
    in the Weather action class returns a list of this entity class.
    This class inherits from the Entity class.
    """

    pass
