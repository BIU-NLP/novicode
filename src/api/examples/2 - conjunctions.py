from ctypes import util
from entities.generic import Contact, DateTime, Location
from typing.navigation import NavigationRoute
from entities.weather import WeatherAttribute
from typing.calendar import CalendarEventName
from typing.timer import Timer
from queries.navigation import NavigationQuery
from queries.weather import WeatherQuery
from queries.messages import MessagesQuery
from queries.calendar import CalendarQuery
from queries.reminders import RemindersQuery
from commands.reminders import RemindersCommand
from commands.responder import ResponderCommand
from commands.timer import TimerCommand
from data_utils import first, last


# Example: "Pause the timer, stop it, and restart it"

timer1 = Timer.resolve_from_text("the timer")
TimerCommand.pause(timer=timer1)

timer2 = Timer.resolve_from_text("it")
TimerCommand.stop(timer=timer2)

timer3 = Timer.resolve_from_text("it")
TimerCommand.restart(timer=timer3)


# Example: "Tell me the weather forecast and delete the last reminder"

weather_forecasts = WeatherQuery.get_weather_forecasts()

ResponderCommand.default_responder(response=weather_forecasts)

reminders = RemindersQuery.get_reminders()
reminders = last(reminders)

RemindersCommand.delete_reminders(reminders=reminders)
