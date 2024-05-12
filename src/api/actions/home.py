from typing import List, Optional, List, Union
from actions.action import Action
from entities.generic import *
from entities.home import *
from providers.data_model import DataModel


class SmartHome(Action):
    """
    The SmartHome class contains all the methods of a virtual assistant agent in the smart home domain.
    This class define a specific API for controlling smart home devices and inherits from the markup Action class.
    The class defines an API to:
    
        * Find smart home devices
        * Execute actions on smart home devices
    """
    
    @classmethod
    def find_home_devices(
        cls,
        device_name: Optional[HomeDeviceName] = None,
        device_action: Optional[HomeDeviceAction] = None,
        device_value: Optional[HomeDeviceValue] = None,
    ) -> List[HomeDeviceEntity]:
        """
        This class method finds smart home devices.

        Parameters
        ----------
        device_name : HomeDeviceName, optional
            The device name
        device_action : HomeDeviceAction, optional
            The action to be performed on the device
        device_value : HomeDeviceValue, optional
            The action's value to be set on the device

        Returns
        -------
        List[HomeDeviceEntity]
            A list of home device entities
        """
        data_model = DataModel()
        data = data_model.get_data(HomeDeviceEntity)

        if device_name:
            data = [x for x in data if x.device_name == device_name]

        if device_action:
            data = [x for x in data if x.device_action == device_action]

        if device_value:
            data = [x for x in data if x.device_value == device_value]

        return data

    @classmethod
    def execute_home_device_action(
        cls,
        date_time: Optional[DateTime] = None,
        device_name: Optional[HomeDeviceName] = None,
        device_action: Optional[HomeDeviceAction] = None,
        device_value: Optional[HomeDeviceValue] = None,
    ) -> HomeDeviceEntity:
        """
        This class method executes given actions on smart home devices.

        Parameters
        ----------
        device_name : HomeDeviceName, optional
            The device name
        device_action : HomeDeviceAction, optional
            The action to be performed on the device
        device_value : HomeDeviceValue, optional
            The action's value to be set on the device
        date_time : DateTime, optional
            The date and time of the action

        Returns
        -------
        HomeDeviceEntity
            Home device entity action is performed on
        """
        home_device = HomeDeviceEntity(
            date_time=date_time,
            device_name=device_name,
            device_action=device_action,
            device_value=device_value,
        )
        data_model = DataModel()
        data_model.append(home_device)
        return home_device
