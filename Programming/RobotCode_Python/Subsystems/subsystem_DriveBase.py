import wpilib
import time

from Subsystems.subsystem_util import PerpetualTimer

class DriveBase:

    MODE_DISABLED = 0
    MODE_ARCADE_COMBINED = 1
    MODE_ARCADE_SPLIT = 2
    MODE_TANK = 3
    MODE_ENCODER = 4
    MODE_VISION = 5
    MODE_IMU = 6
    MODE_COMMAND = 7

    DEFAULT_REFRESH_TIME = 50e-3  # 50 ms

    class arcade_drive:
        def __init__(self, x, y):
            # Calculate the speed
            self.left_speed = self.devices.driver_station.left_joystick.get_y() + \
                         self.devices.driver_station.left_joystick.get_x()
            self.right_speed = self.devices.driver_station.left_joystick.get_y() - \
                          self.devices.driver_station.left_joystick.get_x()

            # Make the speed in range
            self.left_speed = max(min(self.left_speed, 1), -1)
            self.right_speed = max(min(self.right_speed, 1), -1)

    def __init__(self, devices):

        self.devices = devices

        self.mode = self.MODE_DISABLED
        self.refresh_time = self.DEFAULT_REFRESH_TIME

        self.thread = PerpetualTimer(self.refresh_time, self.update)

    def calculate_arcade(self, x, y):


        return {'left_speed':left_speed, 'right_speed': right_speed}

    def update(self):
        left_speed = 0
        right_speed = 0

        if self.mode is self.MODE_DISABLED:
            """ This mode leaves the motor speeds at 0. """
            pass

        elif self.mode is self.MODE_ARCADE_COMBINED:
            """ Uses left joystick only """
            # Calculate the arcade_speeds
            arcade_speeds = self.arcade_drive(x=self.devices.driver_station.left_joystick.get_x(),
                                              y=self.devices.driver_station.left_joystick.get_y())

            # Set the motor output
            left_speed = arcade_speeds.left_speed
            right_speed = arcade_speeds.right_speed

        elif self.mode is self.MODE_ARCADE_SPLIT:
            """
                Uses left joystick for forward/reverse
                Uses right joystick for spin left/right
            """
            arcade_speeds = self.arcade_drive(x=self.devices.driver_station.left_joystick.get_x(),
                                              y=self.devices.driver_station.left_joystick.get_y())

            # Set the motor output
            left_speed = arcade_speeds.left_speed
            right_speed = arcade_speeds.right_speed

        elif self.mode is self.MODE_TANK:
            """ Uses the left and right joystick's y-axis. """
            left_speed = self.devices.driver_station.left_joystick.get_y()
            right_speed = self.devices.driver_station.right_joystick.get_y()

        else:
            """ Catch-all case """
            pass

        self.devices.motors.left_drive.set(left_speed)
        self.devices.motors.right_drive.set(right_speed)

