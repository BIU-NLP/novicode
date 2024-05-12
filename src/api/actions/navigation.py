from __future__ import annotations
from actions.action import Action
from entities.generic import DateTime, Location, TimeDuration
from entities.navigation import *
from typing import List, Optional
from providers.data_model import DataModel


class Navigation(Action):
    """
    The Navigation class contains all the methods of a virtual assistant agent in the navigation domain.
    This class define a specific API for the navigation domain and inherits from the markup Action class.
    This class defines an API to:

        * Find directions between two locations
        * Find the distance between two locations
        * Find the duration between two locations
        * Get the estimated arrival time upon leaving a location at a specific time
        * Get the estimated departure time in order to arrive at a location at a specific time
        * Find the traffic information like traffic jams, accidents, road constructions etc.
    """

    @classmethod
    def find_directions(
        cls,
        destination: Optional[Location],
        origin: Optional[Location] = None,
        departure_date_time: Optional[DateTime] = None,
        avoid_nav_road_condition: Optional[NavigationRoadCondition] = None,
        nav_travel_method: Optional[NavigationTravelMethod] = None,
    ) -> List[NavigationDirectionEntity]:
        """
        This class method find directions based on the given parameters.

        Parameters
        ----------
        destination: Location, optional
            The destination of the navigation
        origin: Location, optional
            The origin of the navigation
        departure_date_time: DateTime, optional
            The date and time the navigation will start
        avoid_nav_road_condition: NavigationRoadCondition, optional
            The road conditions to avoid
        nav_travel_method: NavigationTravelMethod, optional
            The travel method to use

        Returns
        -------
        List[NavigationDirectionEntity]
            A list of directions that were found
        """
        data_model = DataModel()
        data = data_model.get_data(NavigationDirectionEntity)
        if destination:
            data = [x for x in data if x.destination == destination]

        if origin:
            data = [x for x in data if x.origin == origin]

        if departure_date_time:
            data = [x for x in data if x.departure_date_time == departure_date_time]

        if avoid_nav_road_condition:
            data = [
                x
                for x in data
                if x.avoid_nav_road_condition == avoid_nav_road_condition
            ]

        if nav_travel_method:
            data = [x for x in data if x.nav_travel_method == nav_travel_method]

        return data

    @classmethod
    def find_distance(
        cls,
        origin: Optional[Location] = None,
        destination: Optional[Location] = None,
        departure_date_time: Optional[DateTime] = None,
        avoid_nav_road_condition: Optional[NavigationRoadCondition] = None,
        nav_travel_method: Optional[NavigationTravelMethod] = None,
    ) -> List[NavigationDistanceEntity]:
        """
        This class method find the distance between two locations.

        Parameters
        ----------
        origin: Location, optional
            The origin of the navigation
        destination: Location, optional
            The destination of the navigation
        departure_date_time: DateTime, optional
            The date and time the navigation will start
        avoid_nav_road_condition: NavigationRoadCondition, optional
            The road conditions to avoid
        nav_travel_method: NavigationTravelMethod, optional
            The travel method to use

        Returns
        -------
        List[NavigationDistanceEntity]
            A list of distances that were found
        """
        data_model = DataModel()
        data = data_model.get_data(NavigationDistanceEntity)
        if origin:
            data = [x for x in data if x.origin == origin]

        if destination:
            data = [x for x in data if x.destination == destination]

        if departure_date_time:
            data = [x for x in data if x.departure_date_time == departure_date_time]

        if avoid_nav_road_condition:
            data = [
                x
                for x in data
                if x.avoid_nav_road_condition == avoid_nav_road_condition
            ]

        if nav_travel_method:
            data = [x for x in data if x.nav_travel_method == nav_travel_method]

        return data

    @classmethod
    def find_duration(
        cls,
        origin: Optional[Location] = None,
        destination: Optional[Location] = None,
        departure_date_time: Optional[DateTime] = None,
        avoid_nav_road_condition: Optional[NavigationRoadCondition] = None,
        nav_travel_method: Optional[NavigationTravelMethod] = None,
    ) -> List[NavigationDurationEntity]:
        """
        This class method find the the duration of a travel between two locations.

        Parameters
        ----------
        origin: Location, optional
            The origin of the navigation
        destination: Location, optional
            The destination of the navigation
        departure_date_time: DateTime, optional
            The date and time the navigation will start
        avoid_nav_road_condition: NavigationRoadCondition, optional
            The road conditions to avoid
        nav_travel_method: NavigationTravelMethod, optional
            The travel method to use

        Returns
        -------
        List[NavigationDurationEntity]
            A list of durations that were found
        """
        data_model = DataModel()
        data = data_model.get_data(NavigationDurationEntity)
        if origin:
            data = [x for x in data if x.origin == origin]

        if destination:
            data = [x for x in data if x.destination == destination]

        if departure_date_time:
            data = [x for x in data if x.departure_date_time == departure_date_time]

        if avoid_nav_road_condition:
            data = [
                x
                for x in data
                if x.avoid_nav_road_condition == avoid_nav_road_condition
            ]

        if nav_travel_method:
            data = [x for x in data if x.nav_travel_method == nav_travel_method]

        return data

    @classmethod
    def find_estimated_arrival(
        cls,
        origin: Optional[Location] = None,
        destination: Optional[Location] = None,
        arrival_date_time: Optional[DateTime] = None,
        avoid_nav_road_condition: Optional[NavigationRoadCondition] = None,
        nav_travel_method: Optional[NavigationTravelMethod] = None,
    ) -> List[NavigationEstimatedArrivalEntity]:
        """
        This class method gets an estimated arrival information between two locations.

        Parameters
        ----------
        origin: Location, optional
            The origin of the navigation
        destination: Location, optional
            The destination of the navigation
        departure_date_time: DateTime, optional
            The date and time the navigation will start
        avoid_nav_road_condition: NavigationRoadCondition, optional
            The road conditions to avoid
        nav_travel_method: NavigationTravelMethod, optional
            The travel method to use

        Returns
        -------
        List[NavigationEstimatedArrivalEntity]
            A list of estimated arrival information objects that were found
        """
        data_model = DataModel()
        data = data_model.get_data(NavigationEstimatedArrivalEntity)
        if origin:
            data = [x for x in data if x.origin == origin]

        if destination:
            data = [x for x in data if x.destination == destination]

        if arrival_date_time:
            data = [x for x in data if x.arrival_date_time == arrival_date_time]

        if avoid_nav_road_condition:
            data = [
                x
                for x in data
                if x.avoid_nav_road_condition == avoid_nav_road_condition
            ]

        if nav_travel_method:
            data = [x for x in data if x.nav_travel_method == nav_travel_method]

        return data

    @classmethod
    def find_estimated_departure(
        cls,
        origin: Optional[Location],
        destination: Optional[Location],
        arrival_date_time: Optional[DateTime],
        avoid_nav_road_condition: Optional[NavigationRoadCondition],
        nav_travel_method: Optional[NavigationTravelMethod],
    ) -> List[NavigationEstimatedDepartureEntity]:
        """
        This class method gets an estimated departure information between two locations upon
        a target arrival time.

        Parameters
        ----------
        origin: Location, optional
            The origin of the navigation
        destination: Location, optional
            The destination of the navigation
        departure_date_time: DateTime, optional
            The date and time the navigation will start
        avoid_nav_road_condition: NavigationRoadCondition, optional
            The road conditions to avoid
        nav_travel_method: NavigationTravelMethod, optional
            The travel method to use

        Returns
        -------
        List[NavigationEstimatedArrivalEntity]
            A list of estimated departure information objects that were found
        """
        data_model = DataModel()
        data = data_model.get_data(NavigationEstimatedDepartureEntity)
        if origin:
            data = [x for x in data if x.origin == origin]

        if destination:
            data = [x for x in data if x.destination == destination]

        if arrival_date_time:
            data = [x for x in data if x.arrival_date_time == arrival_date_time]

        if avoid_nav_road_condition:
            data = [
                x
                for x in data
                if x.avoid_nav_road_condition == avoid_nav_road_condition
            ]

        if nav_travel_method:
            data = [x for x in data if x.nav_travel_method == nav_travel_method]

        return data

    @classmethod
    def find_traffic_info(
        cls,
        location: Optional[Location] = None,
        origin: Optional[Location] = None,
        destination: Optional[Location] = None,
        date_time: Optional[DateTime] = None,
        departure_date_time: Optional[DateTime] = None,
        nav_road_condition: Optional[NavigationRoadCondition] = None,
        nav_travel_method: Optional[NavigationTravelMethod] = None,
    ) -> List[NavigationTrafficInfoEntity]:
        """
        This class method returns the traffic information on a specific route, location (like road) or a planned
        travel between two locations.

        Parameters
        ----------
        location: Location, optional
            The location along the route to get the traffic information for
        origin: Location, optional
            The origin of the navigation
        destination: Location, optional
            The destination of the navigation
        departure_date_time: DateTime, optional
            The date and time the navigation will start
        nav_road_condition: NavigationRoadCondition, optional
            The road conditions to look for
        nav_travel_method: NavigationTravelMethod, optional
            The travel method to use

        Returns
        -------
        List[NavigationTrafficInfoEntity]
            A list of traffic information objects that were found
        """
        data_model = DataModel()
        data = data_model.get_data(NavigationTrafficInfoEntity)
        if location:
            data = [x for x in data if x.location == location]

        if origin:
            data = [x for x in data if x.origin == origin]

        if destination:
            data = [x for x in data if x.destination == destination]

        if date_time:
            data = [x for x in data if x.date_time == date_time]

        if departure_date_time:
            data = [x for x in data if x.departure_date_time == departure_date_time]

        if nav_road_condition:
            data = [x for x in data if x.nav_road_condition == nav_road_condition]

        if nav_travel_method:
            data = [x for x in data if x.nav_travel_method == nav_travel_method]

        return data
