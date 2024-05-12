from entities.generic import Contact, DateTime, Location
from typing.navigation import NavigationRoute
from entities.weather import WeatherAttribute, WeatherForecastEntity
from typing.calendar import CalendarEventName
from queries.navigation import NavigationQuery
from queries.weather import WeatherQuery
from queries.messages import MessagesQuery
from queries.calendar import CalendarQuery
from commands.reminders import RemindersCommand
from commands.responder import ResponderCommand
from commands.timer import TimerCommand
from data_utils import first, last


"""
Example: "Directions from Monteray to San Francisco"
"""
source = Location.resolve_from_text("Monteray")
destination = Location.resolve_from_text("San Francisco")

directions = NavigationQuery.get_directions(source=source, destination=destination)

ResponderCommand.default_responder(response=directions)


"""
Example: "Tell me the weather in Fairlawn, New Jersey"
"""
location = Location.resolve_from_text("Fairlawn, New Jersey")

weather_forecasts = WeatherQuery.get_weather_forecasts(location=location)

ResponderCommand.default_responder(response=weather_forecasts)


"""
Example: "Check the last message that Kathy sent"
"""
sender = Contact.resolve_from_text("Kathy")

messages = MessagesQuery.get_messages(sender=sender)
message = last(messages)

ResponderCommand.default_responder(response=message)


"""
Example: ”Tell me the weather even though it is early”
"""
weather_forcasts = WeatherQuery.get_weather_forecasts()

ResponderCommand.default_responder(response=weather_forcasts)


"""
Example: "If I take 290 what time will I be in Johnson City?"
"""
route = NavigationRoute.resolve_from_text("290")
destination = Location.resolve_from_text("Johnson City")
estimated_arrival = NavigationQuery.get_estimated_arrival(
    destination=destination, route=route
)
ResponderCommand.default_responder(response=estimated_arrival)


"""
Example: "When I need to leave for class to be there at 8 am"
"""
event_name = CalendarEventName.resolve_from_text("class")
results = CalendarQuery.get_calendar_events(event_name=event_name)
first_result = first(results)
destination = first_result.location

date_time = DateTime.resolve_from_text("8 am")

estimated_departure = NavigationQuery.get_estimated_departure(
    destination=destination, arrival_date_time=date_time
)

ResponderCommand.default_responder(response=estimated_departure)


"""
Example: ”Will it be mostly raining this weekend?”
"""
date_time = DateTime.resolve_from_text("this weekend")
weather_forecasts = WeatherQuery.get_weather_forecasts(date_time=date_time)

weather_attribute = WeatherAttribute.resolve_from_text("raining")
# weather_forecasts2 = filter(
#     WeatherForecastEntity.get_predicate(weather_attribute=weather_attribute),
#     weather_forecasts,
# )

# result = (len(list(weather_forecasts2)) / len(list(weather_forecasts))) > 0.5
result = weather_forecasts.most(weather_attribute=weather_attribute)
response = result
ResponderCommand.default_responder(response=response)


"""
Example: ”Is it going to rain this weekend?”
"""
date_time = DateTime.resolve_from_text("this weekend")
weather_attribute = WeatherAttribute.resolve_from_text("rain")
weather_forecasts = WeatherQuery.get_weather_forecasts(
    date_time=date_time,
    weather_attribute=weather_attribute
)

response = weather_forecasts
ResponderCommand.default_responder(response=result)
def testIter(self):
    data=List()
    data.append(Weather(
        date_time=datetime("2022/10/08"), 
        high_temp=12, 
        low_temp=4, 
        weather_attribute=WeatherAttributes.RAIN
    ))
    data.append(Weather(
        date_time=datetime("2022/10/08"), 
        high_temp=11, 
        low_temp=2, 
        weather_attribute=WeatherAttributes.RAIN
    ))

    self.assertEqual(sum(1 for e in weather_forecasts), 2)
