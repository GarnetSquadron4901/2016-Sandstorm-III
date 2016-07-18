import wpilib


class AnalogPressureSensor(wpilib.AnalogInput):
    DEFAULT_GAIN = 150.0
    DEFAULT_OFFSET = -25.0

    def __init__(self, channel):
        super().__init__(channel=channel)
        self.controller = wpilib.ControllerPower()
        self.gain = self.DEFAULT_GAIN
        self.offset = self.DEFAULT_OFFSET

    def get_instantaneous_pressure_psi(self):
        return self.gain * (super().getVoltage() / self.controller.getVoltage5V()) + self.offset

    def get_pressure_psi(self):
        raise NotImplementedError

    def get_gain(self):
        return self.gain

    def get_offset(self):
        return self.offset

    def set_gain(self, gain):
        self.gain = gain

    def set_offset(self, offset):
        self.offset = offset
