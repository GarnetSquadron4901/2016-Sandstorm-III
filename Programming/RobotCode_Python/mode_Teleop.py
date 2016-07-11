import wpilib
from mode_Init import InitRobot

class Teleop:
    def __init__(self, robot_objects):
        """
        @type robot_objects: InitRobot
        """
        self.robot_objects = robot_objects
