#!/usr/bin/env python3
"""
    robot.py

    This file is the 'main' file for the robot. It will instantiate all of the subsystems and
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

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""

        self.auto_mode = Autonomous(self.robot_objects)

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        self.auto_mode.periodic_update()

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.teleop_mode.periodic_update()

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        self.test_mode.periodic_update()
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
