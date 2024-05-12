from __future__ import annotations
from entities.entity import Entity
from entities.resolvable import Resolvable


class MessageEntity(Entity):
    """
    The MessageEntity class is used to represent a message.
    It is returned by the send_message method in the Message action class,
    or the find_messages method in the Message action class.
    It inherits from the Entity class.
    """

    pass


class MessageStatus(Entity, Resolvable):
    """
    The MessageStatus class is used to represent a message status. A message status can be read or unread.
    It is used in order to filter messages by status in the find_messages method in the Message action class.
    It inherits from the Entity class and the Resolvable class.
    """

    pass


class MessageContentType(Entity, Resolvable):
    """
    The MessageContentType class is used to represent a message content type. A message content type can be text or voice.
    It is used in order to filter messages by content type in the find_messages method in the Message action class. Also,
    it is used in order to specify the content type of a message in the send_message method in the Message action class.
    It inherits from the Entity class and the Resolvable class.
    """

    pass
