from commands.messages import MessagesCommand
from commands.reminders import RemindersCommand
from typing.apps import AppName
from typing.calendar import CalendarEventName
from entities.generic import Contact, DateTime, Location
from entities.message import *
from typing.navigation import TrafficCondition
from typing.reminders import Content
from entities.weather import WeatherAttribute, WeatherForecastEntity, WeatherTemperature
from queries.apps import AppsQuery
from queries.navigation import NavigationQuery
from queries.weather import WeatherQuery
from queries.messages import MessagesQuery
from queries.calendar import CalendarQuery
from queries.reminders import RemindersQuery
from commands.reminders import RemindersCommand
from commands.responder import ResponderCommand
from commands.apps import AppsCommand
from data_utils import first, last


"""
Example: "Remind me to bring a coat, if it rains"
"""

weather_attribute = WeatherAttribute.resolve_from_text("rains")
weather_forecasts = WeatherQuery.get_weather_forecasts(
    weather_attribute=weather_attribute
)
condition = len(list(weather_forecasts)) > 0
if condition:
    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_text("to bring a coat")
    RemindersCommand.create_reminder(person_reminded=person_reminded, content=content)


"""
Example: "Provided that it rains tomorrow set a reminder to leave 15 minutes earlier"
"""

weather_attribute = WeatherAttribute.resolve_from_text("rains")
date_time = DateTime.resolve_from_text("tomorrow")
weather_forecasts = WeatherQuery.get_weather_forecasts(
    date_time=date_time, weather_attribute=weather_attribute
)
condition = len(list(weather_forecasts)) > 0
if condition:
    content = Content.resolve_from_text("to leave 15 minutes earlier")
    RemindersCommand.create_reminder(content=content)


"""
Example: "If it rains then remind me tonight to bring a coat, if it is less than 40 degrees"
"""

weather_attribute = WeatherAttribute.resolve_from_text("rains")
weather_rains = WeatherQuery.get_weather_forecasts(weather_attribute=weather_attribute)
condition = len(list(weather_forecasts)) > 0
if condition:
    temperature = WeatherTemperature.resolve_from_text("less than 40 degrees")
    weather_forecasts = filter(
        WeatherForecastEntity.get_predicate(temperature=temperature), weather_forecasts
    )
    condition = len(list(weather_forecasts)) > 0
    if condition:
        person_reminded = Contact.resolve_from_text("me")
        date_time = DateTime.resolve_from_text("tonight")
        content = Content.resolve_from_text("to leave 15 minutes earlier")
        RemindersCommand.create_reminder(
            date_time=date_time, person_reminded=person_reminded, content=content
        )


"""
Example: "If there is traffic in the city tell Mary that I will be late, otherwise tell her I will be on time"
"""

traffic_condition = TrafficCondition.resolve_from_text("traffic")
location = Location.resolve_from_text("in the city")
traffic_info = NavigationQuery.get_traffic_info(
    location=location, traffic_condition=traffic_condition
)
condition = len(list(traffic_info)) > 0
if condition:
    recipient = Contact.resolve_from_text("Mary")
    content = Content.resolve_from_text("I will be late")
    MessagesCommand.send_message(content=content, recipient=recipient)
else:
    contact = Contact.resolve_from_text("her")
    content = Content.resolve_from_text("I will be on time")
    MessagesCommand.send_message(content=content, recipient=contact)


"""
Example: "Provided that I have a reminder or that I got a message from Jane, start me up the yoga app and tell me when I need to leave for class unless it's raining"
"""

person_reminded = Contact.resolve_from_text("I")
reminder = RemindersQuery.get_reminders(person_reminded=person_reminded)
recipient = Contact.resolve_from_text("I")
sender = Contact.resolve_from_text("Jane")
message = MessagesQuery.get_messages(recipient=recipient, sender=sender)
if reminder or message:
    app_name = AppName.resolve_from_text("the yoga app")
    apps = AppsQuery.get_apps(app_name=app_name)
    app = first(apps)
    AppsCommand.open(app=app)

    weather_attribute = WeatherAttribute.resolve_from_text("raining")
    weather_raining = WeatherQuery.get_weather_forecasts(
        weather_attribute=weather_attribute
    )
    condition = len(list(weather_raining)) > 0
    if not condition:
        event_name = CalendarEventName.resolve_from_text("class")
        events = CalendarQuery.get_calendar_events(event_name=event_name)
        class_event = first(events)
        destination = class_event.location
        estimated_departure = NavigationQuery.get_estimated_departure(
            destination=destination
        )
        ResponderCommand.default_responder(response=estimated_departure)

"""
Delete emails, but only the ones that are unstarred, and archive starred emails.
"""
message_status = MessageStatus.resolve_from_text("unstarred")
