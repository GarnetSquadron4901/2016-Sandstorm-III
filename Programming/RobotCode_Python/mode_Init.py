import wpilib


from Devices.RevRobotics import AnalogPressureSensor
from Devices.Maxbotix.MB10x0 import MB10x0_Digital
from Devices.General import Potentiometer, LimitSwitch
from Devices.AnalogDevices.ADIS16448 import ADIS16488
from Devices.Joysticks.LogitechAttack3 import LogitechAttack3

from Subsystems.subsystem_Arm import Arm
from Subsystems.subsystem_DriveBase import DriveBase
from Subsystems.subsystem_DriverStation import DriverStation
from Subsystems.subsystem_EndEffector import EndEffector
from Subsystems.subsystem_Pneumatics import Pneumatics

class InitRobot:
    def __init__(self):
        self.devices = Devices()
        self.subsystems = Subsystems(self.devices)

class Devices:
    """
    This class initializes the hardware devices on the robot.
    """
    def __init__(self):
        self.motors = self.InitMotors()
        self.sensors = self.InitSensors()
        self.pneumatics = self.InitPneumatics()
        self.driver_station = self.InitDriverStation()

    class InitMotors:
        def __init__(self):
            # PWM Outputs
            self.left_drive = wpilib.Spark(channel=0)
            self.right_drive = wpilib.Spark(channel=1)
            self.grip = wpilib.VictorSP(channel=2)

            # CAN Outputs
            self.arm = wpilib.CANTalon(deviceNumber=2)

    class InitSensors:
        def __init__(self):
            # Digital Inputs
            self.left_drive_encoder = wpilib.Encoder(aChannel=0, bChannel=1)
            self.right_drive_encoder = wpilib.Encoder(aChannel=2, bChannel=3)
            self.lock_disengaged_switch = LimitSwitch(channel=4)
            self.ultrasonic_distance = MB10x0_Digital(channel=5)

            # Analog Inputs
            self.pressure_sensor = AnalogPressureSensor(channel=0)
            self.arm_angle_sensor = Potentiometer(channel=1)

            # XDP sensor
            # self.imu = ADIS16488() - TODO: Finish implementing this class

    class InitPneumatics:
        def __init__(self):
            self.compressor = wpilib.Compressor()
            self.shooter = wpilib.Solenoid(channel=0)
            self.grip = wpilib.Solenoid(channel=1)
            self.arm_lock = wpilib.DoubleSolenoid(forwardChannel=2, reverseChannel=3)

    class InitDriverStation:
        def __init__(self):
            self.left_joystick = LogitechAttack3(0)
            self.right_joystick = LogitechAttack3(1)





class Subsystems:
    def __init__(self, devices):
        """

        :param devices: Devices
        """

        self.arm = Arm(devices)
        self.drive_base = DriveBase(devices)
        self.driver_station = DriverStation(devices)
        self.end_effector = EndEffector(devices)
        self.pneumatics = Pneumatics(devices)
