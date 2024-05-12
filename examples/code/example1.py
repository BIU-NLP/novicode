event_names = EventName.resolve_many_from_text("free events")
date_times = DateTime.resolve_many_from_text("this weekend")
events = []
for event_name in event_names:
    for date_time in date_times:
        events += Calendar.find_events(event_name=event_name, date_time=date_time)
Responder.respond(response=events)

weather_forecasts = Weather.find_weather_forecasts()
Responder.respond(response=weather_forecasts)