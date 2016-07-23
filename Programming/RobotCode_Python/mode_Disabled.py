import wpilib
from mode_Init import InitRobot

class Disabled:
    def __init__(self, robot_objects):
        """
        @type robot_objects: InitRobot
        """

        self.robot_objects = robot_objects

    def init(self):
        pass

    def periodic_update(self):
        self.robot_objects.subsystems.drive_base.do_disabled()


