import wpilib

class AnalogPressureSensor:
    DEFAULT_GAIN = 150.0
    DEFAULT_OFFSET = -25.0

    def __init__(self, channel):
        self.sensor_ai = wpilib.AnalogInput(channel=channel)
        self.controller = wpilib.ControllerPower()
        self.filter = wpilib.LinearDigitalFilter(self.get_instantaneous_pressure_psi, )
        self.gain = self.DEFAULT_GAIN
        self.offset = self.DEFAULT_OFFSET

    def get_vout(self):
        return self.sensor_ai.getVoltage()

    def get_vcc(self):
        return self.controller.getVoltage5V()

    def get_instantaneous_pressure_psi(self):
        return self.gain * (self.get_vout() / self.get_vcc()) + self.offset

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
