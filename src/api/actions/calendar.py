from typing import List, Optional, List, Union
from actions.action import Action
from entities.generic import *
from entities.calendar import *
from providers.data_model import DataModel


class Calendar(Action):
    """
    The Calendar class contains all the methods of a virtual assistant agent in the calendar domain.
    This class define a specific API for the calendar domain and inherits from the markup Action class.
    This class defines an API to:

        * Find events in the calendar
        * Find tickets for events
        * Purchase tickets for events
        * Schedule events in the calendar
        * Delete events from the calendar

    Events in the calendar can be private to the user or public domain events.
    A private event is an event that is scheduled in the user's private calendars (like a peroanl calendar
    or a work calendar). A public event can be a show, a concert, a movie or any other public event that
    is publicly available to the general public.
    """

    @classmethod
    def delete_events(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        event_name: Optional[EventName] = None,
        event_calendar: Optional[EventCalendar] = None,
        event_category: Optional[EventType] = None,
    ) -> List[EventEntity]:
        """
        This class method deletes an event in the calendar.

        Parameters
        ----------
        date_time : DateTime, optional
            The date and time of the event
        location : Location, optional
            The location of the event
        event_name : EventName, optional
            The name of the event
        event_calendar : EventCalendar, optional
            The calendar to search for the event
        event_category : EventType, optional
            The category of the event

        Returns
        -------
        List[EventEntity]
            a list of EventEntity objects that were deleted
        """
        data_model = DataModel()
        events = cls.find_events(
            date_time=date_time,
            location=location,
            event_name=event_name,
            event_calendar=event_calendar,
            event_category=event_category,
        )
        for event in events:
            data_model.delete(event)

        return events

    @classmethod
    def find_events(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        event_name: Optional[EventName] = None,
        event_calendar: Optional[EventCalendar] = None,
        event_category: Optional[EventType] = None,
    ) -> List[EventEntity]:
        """
        This class method finds events in the calendar.

        Parameters
        ----------
        date_time : DateTime, optional
            The date and time of the event
        location : Location, optional
            The location of the event
        event_name : EventName, optional
            The name of the event
        event_calendar : EventCalendar, optional
            The calendar to search for the event
        event_category : EventType, optional
            The category of the event

        Returns
        -------
        List[EventEntity]
            A list of EventEntity objects
        """
        data_model = DataModel()
        data = data_model.get_data(EventEntity)
        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.date_time in date_time]
            else:
                data = [x for x in data if x.date_time == date_time]

        if location:
            data = [x for x in data if x.location == location]

        if event_name:
            data = [x for x in data if x.event_name == event_name]

        if event_calendar:
            data = [x for x in data if x.event_calendar == event_calendar]

        if event_category:
            data = [x for x in data if x.event_category == event_category]

        return data

    @classmethod
    def find_events_tickets(
        cls,
        date_time: Optional[Union[DateTime, List[DateTime]]] = None,
        location: Optional[Location] = None,
        event_name: Optional[EventName] = None,
        event_category: Optional[EventType] = None,
        amount: Optional[Amount] = None,
    ) -> List[EventTicketEntity]:
        """
        This class method finds tickets for events in the calendar.
        It can be used to indicate the availablability of tickets for an event.

        Parameters
        ----------
        date_time : DateTime, optional
            The date and time of the event
        location : Location, optional
            The location of the event
        event_name : EventName, optional
            The name of the event
        event_category : EventType, optional
            The category of the event
        amount : Amount, optional
            The amount of tickets requested for the event

        Returns
        -------
        List[EventTicketEntity]
            A list of EventTicketEntity objects that are available for the event
        """
        data_model = DataModel()
        data = data_model.get_data(EventTicketEntity)
        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.date_time in date_time]
            else:
                data = [x for x in data if x.date_time == date_time]

        if location:
            data = [x for x in data if x.location == location]

        if event_name:
            data = [x for x in data if x.event_name == event_name]

        if event_category:
            data = [x for x in data if x.event_category == event_category]

        if amount:
            data = [x for x in data if x.amount == amount]

        return data

    @classmethod
    def purchase_tickets(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        event_name: Optional[EventName] = None,
        event_category: Optional[EventType] = None,
        amount: Optional[Amount] = None,
    ) -> EventTicketEntity:
        """
        This class method purchase tickets for events in the calendar.

        Parameters
        ----------
        date_time : DateTime, optional
            The date and time of the event
        location : Location, optional
            The location of the event
        event_name : EventName, optional
            The name of the event
        event_category : EventType, optional
            The category of the event
        amount : Amount, optional
            The amount of tickets requested for the event

        Returns
        -------
        List[EventTicketEntity]
            A list of EventTicketEntity objects that were purchased
        """
        event_ticket = EventTicketEntity(
            date_time=date_time,
            location=location,
            event_name=event_name,
            event_category=event_category,
            amount=amount,
        )
        data_model = DataModel()
        data_model.append(event_ticket)
        return event_ticket

    @classmethod
    def schedule_event(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        event_name: Optional[EventName] = None,
        event_calendar: Optional[EventCalendar] = None,
        event_category: Optional[EventType] = None,
    ) -> EventEntity:
        """
        This class method schedules an event in the calendar.

        Parameters
        ----------
        date_time : DateTime, optional
            The date and time of the event
        location : Location, optional
            The location of the event
        event_name : EventName, optional
            The name of the event
        event_calendar : EventCalendar, optional
            The calendar to search for the event
        event_category : EventType, optional
            The category of the event

        Returns
        -------
        EventEntity
            The event that was scheduled
        """
        event = EventEntity(
            date_time=date_time,
            location=location,
            event_name=event_name,
            event_calendar=event_calendar,
            event_category=event_category,
        )
        data_model = DataModel()
        data_model.append(event)
        return event
