import wpilib
import time
import threading

from Subsystems.subsystem_util import PerpetualTimer
from Algorithms import PID

class DriveBase:

    MODE_DISABLED = 'Disabled'
    MODE_ARCADE_COMBINED = 'Joystick 0 - Arcade'
    MODE_ARCADE_SPLIT = 'Joystick 0,1 - Arcade'
    MODE_TANK = 'Joystick 0,1 - Tank'
    MODE_ENCODER = 'Encoder target'
    MODE_VISION = 'Vision target'
    MODE_IMU = 'IMU spin'
    MODE_COMMAND = 'Commanded'
    MODE_TIMEOUT = 'Timed Out'

    DEFAULT_REFRESH_TIME = 50e-3  # 50 ms
    DEFAULT_TIMEOUT = 500E-3 # 500 ms

    DEFAULT_ENCODER_TOLERANCE = 10 # 10 ticks

    class ArcadeDriveCalc:
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
        """

        :param devices: mode_Init:Devices
        """

        self.devices = devices

        self.mode = self.MODE_DISABLED
        self.last_mode = None
        self.refresh_time = self.DEFAULT_REFRESH_TIME

        self.thread_timer = PerpetualTimer(self.refresh_time, self.update)
        self.encoder_event = threading.Event()

        self.timeout = self.DEFAULT_TIMEOUT
        self.last_update = 0.0
        self.safety_config = True

        self.left_encoder_target = 0
        self.right_encoder_target = 0

        # Encoder mode objects
        self.encoder_Kp = 0
        self.encoder_Ki = 0
        self.encoder_Kd = 0
        self.encoder_tolerance = self.DEFAULT_ENCODER_TOLERANCE
        self.left_encoder_pid = PID.PID_Position(Kp=self.encoder_Kp,
                                                 Ki=self.encoder_Ki,
                                                 Kd=self.encoder_Kd,
                                                 output_min=-1,
                                                 output_max=1)
        self.right_encoder_pid = PID.PID_Position(Kp=self.encoder_Kp,
                                                  Ki=self.encoder_Ki,
                                                  Kd=self.encoder_Kd,
                                                  output_min=-1,
                                                  output_max=1)



        self.ds = wpilib.DriverStation.getInstance()

    def do_arcade_combined(self):
        self.mode = self.MODE_ARCADE_COMBINED

    def do_arcade_split(self):
        self.mode = self.MODE_ARCADE_SPLIT

    def do_tank_drive(self):
        self.mode = self.MODE_TANK

    def do_encoder(self, target_left_distance, target_right_distance, wait_for_finish=True):
        self.left_encoder_target = self.devices.sensors.left_drive_encoder.getDistance() + target_left_distance
        self.right_encoder_target = self.devices.sensors.right_drive_encoder.getDistance() + target_right_distance
        self.mode = self.MODE_ENCODER
        if wait_for_finish is True:
            self.encoder_event.clear()
            self.encoder_event.wait()

    def are_encoders_in_range(self):
        return self.left_encoder_target - self.encoder_tolerance <= self.devices.sensors.left_drive_encoder.getDistance() <= self.left_encoder_target + self.encoder_tolerance and \
               self.right_encoeer_target - self.encoder_tolerance <= self.devices.sensors.right_drive_encoder.getDistance() <= self.right_encoeer_target + self.encoder_tolerance

    def set_safety_enabled(self, enable):
        self.safety_config = enable

    def feed_safety_watchdog(self):
        self.last_update = time.time()

    def check_safety(self):
        if self.last_update + self.timeout < time.time():
            self.mode = self.MODE_TIMEOUT

    def check_mode(self):
        if self.mode != self.last_mode:
            print('New Mode: %s' % self.mode)
            if self.last_mode is not None:
                print('Old Mode: %s' % self.last_mode)
            self.last_mode = self.mode

    def update(self):

        self.check_safety()
        self.check_mode()

        # Always set the speed to 0 to begin with.
        left_speed = 0
        right_speed = 0

        try:

            if self.mode is self.MODE_DISABLED:
                """ This mode sets the motor speeds to 0. """
                left_speed = 0
                right_speed = 0

            elif self.mode is self.MODE_ARCADE_COMBINED:
                """ Uses left joystick only """
                # Calculate the arcade_speeds
                arcade_speeds = self.ArcadeDriveCalc(x=self.devices.driver_station.left_joystick.get_x(),
                                                     y=self.devices.driver_station.left_joystick.get_y())

                # Set the motor output
                left_speed = arcade_speeds.left_speed
                right_speed = arcade_speeds.right_speed

            elif self.mode is self.MODE_ARCADE_SPLIT:
                """
                    Uses left joystick for forward/reverse
                    Uses right joystick for spin left/right
                """
                arcade_speeds = self.ArcadeDriveCalc(x=self.devices.driver_station.left_joystick.get_x(),
                                                     y=self.devices.driver_station.left_joystick.get_y())

                # Set the motor output
                left_speed = arcade_speeds.left_speed
                right_speed = arcade_speeds.right_speed

            elif self.mode is self.MODE_TANK:
                """ Uses the left and right joystick's y-axis. """
                left_speed = self.devices.driver_station.left_joystick.get_y()
                right_speed = self.devices.driver_station.right_joystick.get_y()

            elif self.mode is self.MODE_ENCODER:
                # Update the set point
                self.left_encoder_pid.set_setpoint(self.left_encoder_target)
                self.right_encoder_pid.set_setpoint(self.right_encoder_target)

                # Update the process variable
                self.left_encoder_pid.set_processvar(self.devices.sensors.left_drive_encoder.getDistance())
                self.right_encoder_pid.set_processvar(self.devices.sensors.right_drive_encoder.getDistance())

                # Calculate the output
                left_speed = self.left_encoder_pid.update()
                right_speed = self.right_encoder_pid.update()

                if self.mode == self.MODE_ENCODER and not self.are_encoders_in_range():
                    time.sleep(self.refresh_time)

            elif self.mode is self.MODE_VISION:
                # TODO Implement
                pass

            elif self.mode is self.MODE_IMU:
                # TODO Implement
                pass

            elif self.mode is self.MODE_COMMAND:
                # TODO Implement
                pass

            elif self.mode is self.MODE_TIMEOUT:
                """ This mode is set if the drive base watchdog timer expires. """
                left_speed = 0
                right_speed = 0

            else:
                """ Catch-all case """
                left_speed = 0
                right_speed = 0
        except Exception as e:
            self.ds.reportError(e, True)
            left_speed = 0
            right_speed = 0

        self.devices.motors.left_drive.set(left_speed)
        self.devices.motors.right_drive.set(right_speed)

