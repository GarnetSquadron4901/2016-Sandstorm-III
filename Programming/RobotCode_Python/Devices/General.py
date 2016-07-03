import wpilib

class LimitSwitch(wpilib.DigitalInput):
    def __init__(self, dio_port, enable=True, default=False):