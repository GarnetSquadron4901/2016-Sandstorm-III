import wpilib

MM_PER_INCH = 25.4

class MB10x0_Digital(wpilib.Counter, wpilib.Ultrasonic):
    SEC_PER_INCH = 147e-6  # 147 uS
    MAX_PERIOD = 254 * SEC_PER_INCH

    def __init__(self, channel):
        """ Uses the Maxbotix PWM interface to measure distance.

        Compatible with all Maxbotix MB10x0 ultrasonic range finders.

        This class is somewhat hacked to work with the Maxbotix sensor using the wpilib.Counter class.

        The MaxPeriod is set to the maximum range of the sensor. If it goes above this range, it is assumed to be
        disconnected, and the sensor will throw an

        """
        super().__init__(channel)
        super().setMaxPeriod(self.MAX_PERIOD)


    def getRangeInches(self):
        """ Returns the range in inches.  Will throw an exception if the range is too long, signifying a sensor problem.

        Args:

        Returns:
            range (float) - range in inches

        """

        if super().getStopped():
            raise Exception('The sensor\'s range response was too long. Likely the sensor is unplugged or a wire is'
                            'broken')
        return super().getPeriod() / self.SEC_PER_INCH

    def getRangeMM(self):
        """ Returns the range in millimeters using the analog interface.

        Args:

        Returns:
            range (float) - range in millimeters

        """
        return self.getRangeInches() * MM_PER_INCH


class MB10x0_Analog(wpilib.AnalogInput):
    SCALE_FACTOR = 1.0/512.0  # Called the scaling factor, used in (Vcc / 512)

    def __init__(self, channel):
        """ Uses the Maxbotix analog interface to measure distance.

        Compatible with all Maxbotix MB10x0 ultrasonic range finders.

        Uses the measured controller's 5V output to calculate the gain.

        """
        super().__init__(channel)
        self.controller = wpilib.ControllerPower()

    def getRangeInches(self):
        """ Returns the range in inches using the analog interface.

        Args:

        Returns:
            range (float) - range in inches

        """
        return super().getVoltage() / (self.controller.getVoltage5V() * self.SCALE_FACTOR)

    def getRangeMM(self):
        """ Returns the range in millimeters using the analog interface.

        Args:

        Returns:
            range (float) - range in millimeters

        """
        return self.getRangeInches() * MM_PER_INCH


