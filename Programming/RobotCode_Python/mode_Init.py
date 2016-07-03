import wpilib
from subsystem_Arm import Arm
from subsystem_DriverStation import DriverStation
from subsystem_EndEffector import EndEffector
from subsystem_Pneumatics import Pneumatics
from subsystem_DriveBase import DriveBase
from parameter_parser import Parameters


class Motors:
    def __init__(self):
        self.left_drive = wpilib.Spark()


class Sensors:
    def __init__(self):
        pass


class Cylinders:
    def __init__(self):
        pass

