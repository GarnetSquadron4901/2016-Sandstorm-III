import wpilib
from mode_Init import InitRobot

import time

class Autonomous:
    def __init__(self, robot_objects):
        """
        @type robot_objects: InitRobot
        """

        self.robot_objects = robot_objects
        self.auto_loop_counter = 0

    def auto_init(self):
        """ Used right before autonomous. Might be a good place to grab the time or reset encoders. """
        self.start_time = time.time()
        self.auto_loop_counter = 0

    def periodic_update(self):
        self.auto_loop_counter += 1
