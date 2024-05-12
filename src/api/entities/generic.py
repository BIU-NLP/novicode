from __future__ import annotations
from typing import Optional, Union, List
from datetime import datetime
from entities.entity import Entity
from entities.resolvable import Resolvable


class Content(Entity, Resolvable):
    """
    The Content class is used to represent a content like a text, a voice, an image, a video, etc.
    This is a generic class that can be used to represent any content. for exmaple, like in a message
    or a reminder.
    The content can also be casted from any other entity. For example, a driving directions instruction
    can be casted to a content.
    It inherits from the Entity class and the Resolvable class.
    """

    # @classmethod
    # def resolve_from_entity(
    #     cls,
    #     entity: Union[Entity, List[Entity]],
    #     text: Optional[str] = None,
    #     recovered_entity: Optional[Union[Entity, List[Entity]]] = None,
    # ) -> Content:
    #     content = Content(value=entity)
    #     return content
    pass


class Contact(Entity, Resolvable):
    """
    The Contact class is used to represent a contact book contact. A contact is anyone that can be contacted.
    Contacts are used in order to send messages (to and from) or set reminders for.
    Any textual description of a person (or a list of people) can be resolved to a contact (or list of contacts).
    This class inherits from the Entity class and the Resolvable class.
    """

    pass


class DateTime(Entity, Resolvable):
    """
    The DateTime class is used to represent a date and time.
    Many action methods use this class in order to specify a date and time for an action.
    For example:
        * A reminder can be set to a specific date and time.
        * An alarm can be set to a specific date and time.
        * A message can be sent at a specific date and time.
        * A meeting can be scheduled at a specific date and time.
    This class inherits from the Entity class and the Resolvable class.
    """

    pass


class Location(Entity, Resolvable):
    """
    The Location class is used to represent a location. A location can be a place, a city, a country,
    a landmark, a road, etc. Locations can also be a store, a restaurant, a hotel, etc. In contrast to
    a MapEntity, a location does not hold information on a place besides its physical location and its
    name association.
    This class inherits from the Entity class and the Resolvable class.
    """

    pass


class Amount(Entity, Resolvable):
    """
    The Amount class is used to represent an amount of something. An amount can be a number of items.
    It is used in the context of this API to indicate number of tickets to purchase for an event, or
    a number of products to purchase or place in a shopping list. An amout will typically resolve a specific
    amount and is less used in a general quantifier context (like the detrminers "a", "the", etc.).
    It inherits from the Entity class and the Resolvable class.
    """

    pass


class TimeDuration(Entity, Resolvable):
    """
    The TimeDuration class is used to represent a duration of time. A duration of time can be a number of
    minutes to wait when setting a timer. It is used in the API in the context of a timer.
    It inherits from the Entity class and the Resolvable class.
    """

    pass
