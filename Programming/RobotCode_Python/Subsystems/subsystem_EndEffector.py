"""
subsystem_EndEffector.py

This file contains the programming for the end-effector, or what is at the end of our arm.
In this case, it controls the grip motors, claw opening and closing, as well as the shooter.

"""

import wpilib
from wpilib.command import Command

class EndEffector(Command):

    def start(self, devices):
        """
        :param devices: mode_Init:Devices
        """
        self.devices = devices
        super().start()

    def initialize(self):
        pass

    def execute(self):
        pass

    def isFinished(self):
        return False
