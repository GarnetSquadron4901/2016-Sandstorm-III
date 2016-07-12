import wpilib
import time

from Devices.RoboRIO_MXP import MXP_DIO

class ADIS16488(wpilib.InterruptableSensorBase):

    # Pins
    ADIS16488_MXP_RESET_PINT = 8
    ADIS16488_MXP_INT_PIN = 0

    # SPI Settings
    ADIS16488_SPI_CLOCK = 1e6  # 1MHz

    # Time constants
    ADIS16488_RESET_DELAY = 20e-3  # 20 ms

    # Register addresses


    def __init__(self):

        # Setup hardware interface
        self.imu_spi = wpilib.SPI(port=wpilib.SPI.Port.kMXP)
        self.imu_spi.setClockRate(self.ADIS16488_SPI_CLOCK)
        self.imu_spi.setClockActiveLow()
        self.imu_spi.setSampleDataOnFalling()

        self.imu_reset_pin = wpilib.DigitalOutput(channel=MXP_DIO[self.ADIS16488_MXP_RESET_PINT])

        self.imu_int_pin = wpilib.DigitalSource(channel=MXP_DIO[self.ADIS16488_MXP_INT_PIN], input=True)
        super().
        super().setUpSourceEdge(risingEdge=False, fallingEdge=True)

        # Reset the IMU
        self.reset()



    def reset(self):
        self.imu_reset_pin.set(False)
        time.sleep(self.ADIS16488_RESET_DELAY)
        self.imu_reset_pin.set(True)

    def getTemperature(self):
        raise NotImplementedError

    def getGyro(self):
        raise NotImplementedError

    def getAccelerometer(self):
        raise NotImplementedError

    def getMagnetometer(self):
        raise NotImplementedError

    def getBarometer(self):
        raise NotImplementedError

    def getStatus(self):
        pass

    def getID1(self):
        pass

    def getID2(self):
        pass

    def getProductId(self):
        pass

    def getSerial(self):
        pass




