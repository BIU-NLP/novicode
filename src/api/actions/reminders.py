from typing import Any, List, Mapping, Union, Optional
from actions.action import Action
from entities.generic import *
from entities.reminder import *
from providers.data_model import DataModel


class Reminders(Action):
    """
    The Reminders class contains all the methods of a virtual assistant agent in the reminders domain.
    This class define a specific API for the reminders domain and inherits from the markup Action class.
    This class defines an API to:

        * Create a reminder
        * Find reminders
        * Delete reminders

    Reminders are associated with a reminded person, a reminded content and a date time.
    """

    @classmethod
    def create_reminder(
        cls,
        content: Optional[Content] = None,
        person_reminded: Optional[Contact] = None,
        date_time: Optional[DateTime] = None,
    ) -> ReminderEntity:
        """
        This class method creates a reminder.

        Parameters
        ----------
        content : Content, Optional
            The content of the reminder.
        person_reminded : Contact, optional
            The person to be reminded.
        date_time : DateTime, optional
            The date and time of the reminder.

        Returns
        -------
        ReminderEntity
            The reminder entity object that was created
        """
        reminder = ReminderEntity(
            date_time=date_time,
            person_reminded=person_reminded,
            content=content,
        )
        data_model = DataModel()
        data_model.append(reminder)
        return reminder

    @classmethod
    def find_reminders(
        cls,
        person_reminded: Optional[Contact] = None,
        date_time: Optional[DateTime] = None,
        content: Optional[Content] = None,
    ) -> List[ReminderEntity]:
        """
        This class method finds existing reminders.

        Parameters
        ----------
        content : Content
            The content of the reminder.
        person_reminded : Contact, optional
            The person to be reminded.
        date_time : DateTime, optional
            The date and time of the reminder.

        Returns
        -------
        List[ReminderEntity]
            A list of reminder entity objects that were found
        """
        data_model = DataModel()
        data = data_model.get_data(ReminderEntity)
        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.date_time in date_time]
            else:
                data = [x for x in data if x.date_time == date_time]

        if person_reminded:
            data = [x for x in data if x.person_reminded == person_reminded]

        if content:
            data = [x for x in data if x.content == content]

        return data

    @classmethod
    def delete_reminders(
        cls, reminders: Union[ReminderEntity, List[ReminderEntity]]
    ) -> List[ReminderEntity]:
        """
        This class method delete reminders.

        Parameters
        ----------
        reminders : Union[ReminderEntity, List[ReminderEntity]]
            The reminders to be deleted. Can be a single reminder or a list of reminders.

        Returns
        -------
        List[ReminderEntity]
            The list of reminders that were deleted
        """
        data_model = DataModel()
        if reminders:
            if type(reminders) == list:
                for reminder in reminders:
                    data_model.delete(reminder)
            else:
                data_model.delete(reminder)
        
        data = data_model.get_data(ReminderEntity)
        return data
