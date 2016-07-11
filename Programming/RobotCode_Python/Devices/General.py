import wpilib

class LimitSwitch(wpilib.DigitalInput):
    TYPE_NORMALLY_CLOSED = False
    TYPE_NORMALLY_OPEN = True

    def __init__(self, channel, switch_type=TYPE_NORMALLY_CLOSED):
        super().__init__(channel)
        self.type = switch_type

    def getSwitchState(self):
        return super().get() != self.type

class Potentiometer(wpilib.AnalogInput):
    DEFAULT_DEGREE_RANGE = 270

    def __init__(self, channel, range=None, invert=False):
        super().__init__(channel)
        self.controller = wpilib.ControllerPower()

        if range is not None:
            self.range = range
        else:
            self.range = self.DEFAULT_DEGREE_RANGE

        self.invert = invert

    def getReferenceVoltage(self):
        return self.controller.getVoltage5V()

    def getPercentage(self):
        if not self.invert:
            return super().getVoltage() / self.getReferenceVoltage()
        else:
            return (self.getReferenceVoltage() - super().getVoltage()) / self.getReferenceVoltage()

    def getAngle(self):
            return self.getPercentage() * self.range



