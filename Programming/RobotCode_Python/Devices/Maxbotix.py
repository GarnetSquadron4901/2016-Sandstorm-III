import wpilib

class MB10x0_Digital:
    US_PER_INCH = 147
    def __init__(self, channel):
        self.sensor_
        self.sesnor_ai = wpilib.Counter()

class MB10x0_Analog(wpilib.AnalogInput):
    SCALE_FACTOR = 1.0/512.0 # Called the scaling factor, used in (Vcc / 512)

    def __init__(self, channel):
        super().__init__(channel)
        self.controller = wpilib.ControllerPower()

    def get_range(self):

    def get_gain(self):
        return self.controller.getVoltage5V() / self.SCALE_FACTOR

