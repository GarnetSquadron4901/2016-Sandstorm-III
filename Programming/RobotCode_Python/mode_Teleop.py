import wpilib
from mode_Init import InitRobot

class Teleop:
    def __init__(self, robot_objects):
        """
        @type robot_objects: InitRobot
        """
        self.robot_objects = robot_objects

    def periodic_update(self):
        # Set the drive mode to manual mode, arcade split
        self.robot_objects.subsystems.drive_base.do_arcade_split()
