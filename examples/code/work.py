# If it rains tomorrow then text Alice

weather_attribute = WeatherAttribute.resolve_many_from_text("rains")
date_time = DateTime.resolve_from_text("tomorrow")
weather_forecasts = Weather.find_weather_forecasts(
    weather_attribute=weather_attribute, date_time=date_time
)
test = bool(weather_forecasts)
if test:
    recipient = Contact.resolve_from_text("Alice")
    Messages.send_message(recipient=recipient)
