from itertools import groupby
from typing.calendar import (
    CalendarEvent,
    CalendarEventType,
    CalendarEventName,
    CalendarName,
)
from entities.generic import Contact, DateTime, Location
from typing.message import Content
from typing.navigation import TrafficCondition
from typing.reminders import Content
from entities.weather import WeatherAttribute, WeatherTemperature
from queries import calendar, messages, navigation, reminders, weather
from queries.calendar import CalendarQuery
from queries.navigation import NavigationQuery
from queries.weather import WeatherQuery
from commands.calendar import CalendarCommand
from commands.messages import MessagesCommand
from commands.reminders import RemindersCommand
from commands.responder import ResponderCommand
from data_utils import first, last, day_of_the_week
from exceptions.exceptions import NoSuchValueException

"""
Execution exception example: Cancel all my meetings on February 30
"""
try:
    date_time = DateTime.resolve_from_text(
        "February 30"
    )  # <- should raise recovery exception
    events = CalendarQuery.get_calendar_events(date_time=date_time)
    CalendarCommand.delete_calendar_events(events=events)
except NoSuchValueException as e:
    pass

"""
Execution exception example: Provided that it rains tomorrow set a reminder
"""

weather_attribute = WeatherAttribute.resolve_from_text("rains")
date_time = DateTime.resolve_from_text("tomorrow")
weather_rains = WeatherQuery.get_weather_forecasts(
    date_time=date_time, weather_attribute=weather_attribute
)

if weather_rains:
    RemindersCommand.create_reminder()  # <- should raise recovery exception

"""
Example: "If there is traffic tell Mary that I will be late"
"""

traffic_condition = TrafficCondition.resolve_from_text("traffic")
traffic_info = NavigationQuery.get_traffic_info(
    traffic_condition=traffic_condition
)  # <- should raise recovery exception

if traffic_info:
    recipient = Contact.resolve_from_text("Mary")
    content = Content.resolve_from_text("I will be late")
    MessagesCommand.send_message(content=content, recipient=recipient)
