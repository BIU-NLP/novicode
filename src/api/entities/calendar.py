from __future__ import annotations
from typing import Callable, Optional
from abc import abstractclassmethod
from entities.generic import Contact, Content, DateTime, Location
from entities.entity import Entity
from entities.resolvable import Resolvable


class EventName(Entity, Resolvable):
    """
    The EventName class is used to represent an event name. An event name can be a specific name or a generic name.
    It can also be a private event name. For example, "my birthday party" or "the meeting". And a public domain
    event like "the super bowl".
    It inherits from the Entity class and the Resolvable class.
    """

    pass


class EventCalendar(Entity, Resolvable):
    """
    The EventCalendar class is used to represent an event calendar. For example, "my personal calendar" or "my work calendar".
    An event calendar can be a specific calendar to schedule an event on, or to find events in.
    It inherits from the Entity class and the Resolvable class.
    """

    pass


class EventType(Entity, Resolvable):
    """
    The EventType class is used to represent an event type. It should not be used and is kept for backward compatibility.
    """

    pass


class EventEntity(Entity):
    """
    The EventEntity class is used to represent an event. It is returned by the find_events method.
    It inherits from the Entity class.
    """

    pass


class EventTicketEntity(Entity):
    """
    The EventTicketEntity class is used to represent an event ticket. It is returned by the find_event_tickets method.
    It inherits from the Entity class.
    """

    pass
