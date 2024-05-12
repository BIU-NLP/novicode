from typing import List, Union, Optional
from actions.action import Action
from entities.generic import *
from entities.message import *
from entities.app import App
from providers.data_model import DataModel


class Messages(Action):
    """
    The Messages class contains all the methods of a virtual assistant agent in the messages domain.
    This class define a specific API for the messages domain and inherits from the markup Action class.
    This class defines an API to:

        * Find messages
        * Send messages
        * Delete messages

    Messages are sent to a recipient, from a sender, at a specific date and time. The messages can be sent
    from a specific application (like email, the messages app in the smart phone, or Whatsapp). Messages
    include a content, an attachment and a content type (text, image, video, etc.). Messages can have a
    status (sent, open).
    """

    @classmethod
    def find_messages(
        cls,
        date_time: Optional[DateTime] = None,
        sender: Optional[Contact] = None,
        recipient: Optional[Contact] = None,
        content: Optional[Content] = None,
        message_status: Optional[MessageStatus] = None,
        message_content_type: Optional[MessageContentType] = None,
        app: Optional[App] = None,
    ) -> List[MessageEntity]:
        """
        This class method find messages based on the given parameters.

        Parameters
        ----------
        date_time : DateTime, optional
            The date and time the message will be sent
        sender : Contact, optional
            The sender of the message
        recipient : Contact, optional
            The recipient of the message
        content : Content, optional
            The content of the message
        message_status : MessageStatus, optional
            The status of the message (e.g., open, send, read, unread)
        message_content_type : MessageContentType, optional
            The content type of the message
        app : App, optional
            The application used to send the message

        Returns
        -------
        List[MessageEntity]
            The list of messages that were found
        """
        data_model = DataModel()
        data = data_model.get_data(MessageEntity)
        if date_time:
            data = [x for x in data if x.date_time == date_time]

        if sender:
            data = [x for x in data if x.sender == sender]

        if recipient:
            data = [x for x in data if x.recipient == recipient]

        if content:
            data = [x for x in data if x.content == content]

        if message_status:
            data = [x for x in data if x.message_status == message_status]

        if message_content_type:
            data = [x for x in data if x.message_content_type == message_content_type]

        if app:
            data = [x for x in data if x.app == app]

        return data

    @classmethod
    def send_message(
        cls,
        recipient: Optional[Contact] = None,
        content: Optional[Content] = None,
        date_time: Optional[DateTime] = None,
        message_content_type: Optional[MessageContentType] = None,
    ) -> MessageEntity:
        """
        This class method send messages.

        Parameters
        ----------
        recipient : Contact, optional
            The recipient of the message
        content : Content, optional
            The content of the message
        date_time : DateTime, optional
            The date and time the message will be sent
        message_content_type : MessageContentType, optional
            The content type of the message

        Returns
        -------
        MessageEntity
            The message that was sent
        """
        message = MessageEntity(
            date_time=date_time,
            recipient=recipient,
            content=content,
            message_content_type=message_content_type,
        )
        data_model = DataModel()
        data_model.append(message)
        return message

    @classmethod
    def delete_messages(
        cls, messages: Union[MessageEntity, List[MessageEntity]]
    ) -> List[MessageEntity]:
        """
        This class method deletes messages.

        Parameters
        ----------
        messages : MessageEntity|List[MessageEntity], optional
            The messages to be deleted. If a single message is passed, it will be converted to a list.

        Returns
        -------
        List[MessageEntity]
            a list of MessageEntity objects that were deleted
        """
        data_model = DataModel()
        if isinstance(messages, MessageEntity):
            messages = [messages]

        for message in messages:
            data_model.delete(message)
