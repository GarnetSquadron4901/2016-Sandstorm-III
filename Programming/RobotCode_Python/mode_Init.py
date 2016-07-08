import wpilib
from Devices.RevRobotics import AnalogPressureSensor
from subsystem_Arm import Arm
from subsystem_DriverStation import DriverStation
from subsystem_EndEffector import EndEffector
from subsystem_Pneumatics import Pneumatics
from subsystem_DriveBase import DriveBase
from parameter_parser import Parameters

class Init:
    def __init__(self):
        self.motors = InitMotors()
        self.sensors = InitSensors()
        self.pneumatics = InitPneumatics()


class InitMotors:
    def __init__(self):
        self.left_drive = wpilib.Spark(channel=0)
        self.right_drive = wpilib.Spark(channel=1)
        self.arm = wpilib.CANTalon(deviceNumber=2)
        self.grip = wpilib.VictorSP(channel=2)


class InitSensors:
    def __init__(self):
        self.left_drive_encoder = wpilib.Encoder(aChannel=0, bChannel=1)
        self.right_drive_encoder = wpilib.Encoder(aChannel=2, bChannel=3)
        self.lock_disengaged_switch = wpilib.DigitalInput(channel=4)
       # self.ultrasonic_distance = wpilib.??? We need something to measure a PWM input.
        self.pressure_sensor = AnalogPressureSensor()



class InitPneumatics:
    def __init__(self):
        self.compressor = wpilib.Compressor()

