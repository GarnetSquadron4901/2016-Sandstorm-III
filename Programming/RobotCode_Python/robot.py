#!/usr/bin/env python3
"""
    robot.py

    This file is the 'main' file for the robot.
"""

import wpilib

from mode_Init import InitRobot
from mode_Autonomous import Autonomous
from mode_Disabled import Disabled
from mode_Teleop import Teleop
from mode_Test import Test


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.robot_objects = InitRobot()
        self.auto_mode = Autonomous(self.robot_objects)
        self.teleop_mode = Teleop(self.robot_objects)
        self.disabled_mode = Disabled(self.robot_objects)
        self.test_mode = Test(self.robot_objects)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""

        self.auto_mode.auto_init()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        self.auto_mode.periodic_update()

    def teleopInit(self):
        self.teleop_mode.init()

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.teleop_mode.periodic_update()

    def testInit(self):
        self.test_mode.init()

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        self.test_mode.periodic_update()
        wpilib.LiveWindow.run()

    def disabledInit(self):
        self.disabled_mode.init()

    def disabledPeriodic(self):
        self.disabled_mode.periodic_update()



    def free(self):
        self.robot_objects.subsystems.drive_base.thread_timer.cancel()

if __name__ == "__main__":
    wpilib.run(MyRobot)
