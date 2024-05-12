from typing import List, Union
from actions.action import Action
from entities.generic import Entity
from providers.data_model import DataModel


class Responder(Action):
    """
    Responders are used to respond to user requests. Responder is the default way to react to user requests that
    requires a response. Any entities recieved from the APIs can be passed to the responder to be sent to the user.
    """

    @classmethod
    def respond(cls, response: Union[List[Entity], Entity]) -> None:
        """
        This class method delete reminders.

        Parameters
        ----------
        response : Union[List[Entity], Entity]
            The entity or a list of entities to be sent to the user.

        Returns
        -------
        None
        """
        data_model = DataModel()
        data_model.append_output_data(response)
