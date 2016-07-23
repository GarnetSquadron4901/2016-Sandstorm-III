import wpilib
from wpilib.command import Command

class DriverStation(Command):

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
