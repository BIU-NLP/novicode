from typing import List, Optional, List, Union
from actions.action import Action
from entities.generic import DateTime, Location
from entities.weather import *
from providers.data_model import DataModel


class Weather(Action):
    """
    The Weather class contains all the methods of a virtual assistant agent in the weather domain.
    This class define a specific API for the weather domain and inherits from the markup Action class.
    This class defines an API to:

        * Find weather forecasts
        
    A weather forecast often includes a date and time of the forecast, the location for which the forecast is made,
    a weather attribute (like rain, sunny, cold, etc.), and a weather temperature.
    """
    
    @classmethod
    def find_weather_forecasts(
        cls,
        date_time: Optional[Union[DateTime, List[DateTime]]] = None,
        location: Optional[Location] = None,
        weather_attribute: Optional[WeatherAttribute] = None,
        weather_temperature: Optional[WeatherTemperature] = None,
    ) -> List[WeatherForecastEntity]:
        """
        This class method find weather forecasts based on the given parameters.

        Parameters
        ----------
        date_time : DateTime, optional
            The date and time to forecast the weather at
        location : Location, optional
            The location to forecast the weather at
        weather_attribute : WeatherAttribute, optional
            The weather attribute to forecast (e.g., rain, sunny, cold, etc.)
            This parameter can be used to filter the weather forecast on a specific weather attribute
        weather_temperature : WeatherTemperature, optional
            The weather temperature to forecast (e.g., less than 80 degrees)
            This parameter can be used to filter the weather forecast on a specific weather termperature
            
        Returns
        -------
        List[WeatherForecastEntity]
            The list of weather forecasts that were found
        """
        data_model = DataModel()
        data = data_model.get_data(WeatherForecastEntity)
        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.date_time in date_time]
            else:
                data = [x for x in data if x.date_time == date_time]

        if location:
            data = [x for x in data if x.location == location]

        if weather_attribute:
            data = [x for x in data if x.weather_attribute == weather_attribute]

        if weather_temperature:
            data = [
                x
                for x in data
                if x.weather_temperature == weather_temperature
            ]

        return data
