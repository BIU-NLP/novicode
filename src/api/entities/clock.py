from entities.resolvable import Resolvable
from entities.entity import Entity


class TimerEntity(Entity):
    """
    The TimerEntity class is used to represent a timer.
    The timer can be updated, paused, resumed or stopped.
    It inherits from the Entity class.
    """

    pass


class AlarmEntity(Entity):
    """
    The AlarmEntity class is used to represent an alarm.
    It is created by the create_alarm method in the Alarm action class.
    It inherits from the Entity class.
    """

    pass


class AlarmName(Entity, Resolvable):
    """
    The AlarmName class is used to represent an alarm name. An alarm name is
    used to identify an alarm and to be able to search it by its associated name.
    For example, an alarm name appear as "the 6:30 alarm" in the clock app.
    It inherits from the Entity class and the Resolvable class.
    """

    pass
