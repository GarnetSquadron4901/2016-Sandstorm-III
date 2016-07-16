import wpilib
import time
import struct
from threading import Thread



from Devices.RoboRIO_MXP import MXP_DIO




class ADIS16488(wpilib.InterruptableSensorBase):

    ############################################
    ## Constants
    ############################################

    # Pins
    ADIS16488_MXP_RESET_PINT = 8
    ADIS16488_MXP_INT_PIN = 0


    # Time constants
    ADIS16488_RESET_DELAY = 20e-3  # 20 ms


    class ImuNotPresentError(Exception):
        pass


    class ADIS16488_IMU:
        # Registers
        ADIS16488_REG_GLOB_CMD = 0x3e
        ADIS16488_REG_SMPL_PRD = 0x36
        ADIS16488_REG_SENS_AVG = 0x38
        ADIS16488_REG_MSC_CTRL = 0x34
        ADIS16488_REG_PROD_ID = 0x56

        # SPI Settings
        ADIS16488_SPI_CLOCK = 1e6  # 1MHz

        # ADIS16588 Product ID
        ADIS16488_PROD_ID_VAL = 16488

        def __init__(self):
            self.ds = wpilib.DriverStation()

            # Setup SPI hardware interface
            self.imu_spi = wpilib.SPI(port=wpilib.SPI.Port.kMXP)
            self.imu_spi.setClockRate(self.ADIS16488_SPI_CLOCK)
            self.imu_spi.setMSBFirst()
            self.imu_spi.setSampleDataOnFalling()
            self.imu_spi.setClockActiveLow()
            self.imu_spi.setChipSelectActiveLow()

            self.prod_id = self.read_register(self.ADIS16488_REG_PROD_ID)

            if self.prod_id != self.ADIS16488_PROD_ID_VAL:
                self.imu_spi.free()
                del self.imu_spi
                self.ds.reportError('ADIS16488 was not detected')
                raise super().ImuNotPresentError()


        def read_register(self, reg):
            # We need to make the register into a byte array in order to send it over SPI
            write_buf = struct.pack('>', [reg & 0x7f, 0x00])

            self.imu_spi.write(write_buf, 2)

            # Now that the device knows the register to read, wait on it to send me something
            self.imu_spi.read(False, buf, 2)

            return struct.pack('s', buf) & 0xffff  # masks it as a short


    def __init__(self):



        # Setup reset pin

        self.imu_reset_pin = wpilib.DigitalOutput(channel=MXP_DIO[self.ADIS16488_MXP_RESET_PINT])

        # Configure interrupt
        self.imu_int_pin = wpilib.DigitalSource(channel=MXP_DIO[self.ADIS16488_MXP_INT_PIN], input=True)
        self.imu_int_pin.requestInterrupts()
        self.imu_int_pin.setUpSourceEdge(False, True)
        self.imu_int_thread = Thread(target=self._imu_task)
        self.imu_int_thread.setDaemon()
        self.imu_int_thread.start()

        # Reset the IMU
        self.reset()

    def _imu_task(self):
        while True:
            self.calculate()

    def calculate(self):
        pass


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




