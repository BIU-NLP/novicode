events = Calendar.resolve_many_from_text("After every Astros game")
for event in events:
    date_time = DateTime.resolve_from_entity(event)
    content = Content.resolve_from_text("check the traffic")
    Reminders.create_reminder(date_time=date_time, content=content)