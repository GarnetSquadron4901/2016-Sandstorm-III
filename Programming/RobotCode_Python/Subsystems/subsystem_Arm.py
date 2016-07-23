import wpilib
from wpilib.command import Command


class Arm(Command):

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
