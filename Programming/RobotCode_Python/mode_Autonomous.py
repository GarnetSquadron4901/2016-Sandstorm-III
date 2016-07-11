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

    def periodic_update(self):
        if auto_loop_counter == 0:
            self.start_time = time.time()


        self.auto_loop_counter += 1
