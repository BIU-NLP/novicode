from __future__ import annotations
from entities.entity import Entity
from entities.resolvable import Resolvable


class AppName(Entity, Resolvable):
    """
    The App class is used to represent an app. different actions can be performed on an app.
    It is used to indicate the app performing the action.
    It inherits from the Entity class and the Resolvable class.
    """

    pass


class App(Entity):
    """
    The App class is used to represent an app. App entities are returned by the find_apps method in the App action class.
    It inherits from the Entity class.
    """

    pass
