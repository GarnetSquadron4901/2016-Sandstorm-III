import wpilib
import time

from mode_Init import Devices
from Subsystems.subsystem_util import PerpetualTimer

class DriveBase:

    MODE_DISABLED = 0
    MODE_ARCADE_COMBINED = 1
    MODE_ARCADE_SPLIT = 2
    MODE_TANK = 3
    MODE_ENCODER = 4
    MODE_VISION = 5
    MODE_IMU = 6
    MODE_COMMAND = 7

    DEFAULT_REFRESH_TIME = 50e-3  # 50 ms

    def __init__(self, devices):
        """

        @type devices: Devices
        """
        self.devices = devices

        self.mode = self.MODE_DISABLED
        self.refresh_time = self.DEFAULT_REFRESH_TIME

        self.thread = PerpetualTimer(self.refresh_time, self.update)

    def update(self):
        if self.mode is self.MODE_DISABLED:
            self.devices.motors.left_drive.disable()
            self.devices.motors.right_drive.disable()

        if self.mode is self.MODE_ARCADE_COMBINED:


