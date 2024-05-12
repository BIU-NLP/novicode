from typing import List, Union, Optional
from actions.action import Action
from entities.generic import *
from entities.map import *
from providers.data_model import DataModel


class Map(Action):
    """
    The Map class contains all the methods of a virtual assistant agent in the map domain.
    This class define a specific API for finding places on a map and getting information on these places.
    The class defines an API to:

        * Find places on a map
    """

    @classmethod
    def find_on_map(cls, location: Location) -> List[MapEntity]:
        """
        This class method finds places on the map.

        Parameters
        ----------
        location : Location
            The location to search for

        Returns
        -------
        List[MapEntity]
            A list of places in the form of map entities
        """
        data_model = DataModel()
        data = data_model.get_data(MapEntity)
        if location:
            data = [x for x in data if x.location == location]

        return data
