from abc import abstractclassmethod
from actions.action import Action
from typing import List, Union, Optional
from entities.generic import *
from entities.clock import *
from entities.music import *
from providers.data_model import DataModel


class Timer(Action):
    """
    The Timer class contains all the methods of a virtual assistant agent for using a timer in the clock domain.
    This class define a specific API for using the timer and inherits from the markup Action class.
    This class defines an API to:

        * Create a timer
        * Pause a timer
        * Restart a timer
        * Stop a timer
    """

    @classmethod
    def create_timer(
        cls,
        duration: Optional[TimeDuration] = None,
        date_time: Optional[DateTime] = None,
    ) -> TimerEntity:
        """
        This class method creates a timer.
        A timer can be defined with a duration or a date and time.
        If date and time are not specified, the timer will start immediately.

        Parameters
        ----------
        duration : TimeDuration, optional
            The duration of the timer.
        date_time : DateTime, optional
            The date and time of the timer.

        Returns
        -------
        TimerEntity
            The timer entity object
        """
        timer = TimerEntity(
            duration=duration,
            date_time=date_time,
        )
        data_model = DataModel()
        data_model.append(timer)
        return timer

    @classmethod
    def pause(
        cls,
        timer: Optional[TimerEntity] = None,
    ) -> TimerEntity:
        """
        This class method pauses a timer.

        Parameters
        ----------
        timer : Timer, optional
            The timer to be paused

        Returns
        -------
        TimerEntity
            The timer object that was paused
        """
        return NotImplementedError

    @classmethod
    def restart(
        cls,
        timer: Optional[TimerEntity] = None,
    ) -> bool:
        """
        This class method restarts a timer.

        Parameters
        ----------
        timer : Timer, optional
            The timer to be restarted

        Returns
        -------
        TimerEntity
            The timer object that was paused
        """
        raise NotImplementedError

    @classmethod
    def stop(
        cls,
        timer: Optional[TimerEntity] = None,
    ) -> bool:
        """
        This class method stops a timer.

        Parameters
        ----------
        timer : Timer, optional
            The timer to be stopped

        Returns
        -------
        TimerEntity
            The timer object that was paused
        """
        raise NotImplementedError


class Alarm:
    """
    The Alarm class contains all the methods of a virtual assistant agent for using a timer in the clock domain.
    This class define a specific API for using the timer and inherits from the markup Action class.
    This class defines an API to:

        * Create a timer
        * Pause a timer
        * Restart a timer
        * Stop a timer
    """

    @classmethod
    def create_alarm(
        cls,
        alarm_name: Optional[AlarmName] = None,
        date_time: Optional[DateTime] = None,
        song: Optional[Song] = None,
        content: Optional[Content] = False,
    ) -> AlarmEntity:
        """
        This class method creates an alarm.
        An alarm is defined with a date and time and can optionally play a song or present a content.

        Parameters
        ----------
        alarm_name: AlarmName, optional
            The name of the alarm.
        date_time : DateTime, optional
            The date and time of the alarm.
        song : Song, optional
            The song to be played when the alarm is triggered.
        content : Content, optional
            The content to be presented when the alarm is triggered.

        Returns
        -------
        AlarmEntity
            The alarm entity object
        """
        alarm = AlarmEntity(
            alarm_name=alarm_name, date_time=date_time, song=song, content=content
        )
        data_model = DataModel()
        data_model.append(alarm)
        return alarm

    @classmethod
    def update_alarm(
        cls,
        date_time: Optional[DateTime] = None,
        alarm_name: Optional[AlarmName] = None,
    ) -> AlarmEntity:
        """
        This class method updates an alarm.

        Parameters
        ----------
        date_time : DateTime, optional
            The date and time of the alarm.
        alarm_name : AlarmName, optional
            The alarm name.

        Returns
        -------
        AlarmEntity
            The alarm entity object that was updated
        """
        alarm = AlarmEntity(date_time=date_time, alarm_name=alarm_name)
        data_model = DataModel()
        data_model.append(alarm)
        return alarm

    @classmethod
    def find_alarms(
        cls,
        date_time: Optional[DateTime],
        alarm_name: Optional[AlarmName],
    ) -> List[AlarmEntity]:
        """
        This class method finds existing alarms based on the provided parameters.

        Parameters
        ----------
        date_time : DateTime, optional
            The date and time of the alarm.
        alarm_name : AlarmName, optional
            The alarm name.

        Returns
        -------
        List[AlarmEntity]
            The alarm entity object that was updated
        """
        data_model = DataModel()
        data = data_model.get_data(AlarmEntity)
        if date_time:
            data = [x for x in data if x.date_time == date_time]

        if alarm_name:
            data = [x for x in data if x.alarm_name == alarm_name]

        return data
