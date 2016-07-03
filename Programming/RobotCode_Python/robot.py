#!/usr/bin/env python3
"""
    robot.py

    This file is the 'main' file for the robot. It will instantiate all of the subsystems and
"""

import wpilib

from mode_Init import Devices
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
        self.devices =

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.auto_loop_counter = 0
        self.auto_mode = Autonomous()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        
        # Check if we've completed 100 loops (approximately 2 seconds)
        if self.auto_loop_counter < 100:
            self.robot_drive.drive(-0.5, 0) # Drive forwards at half speed
            self.auto_loop_counter += 1
        else:
            self.robot_drive.drive(0, 0)    #Stop robot

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.robot_drive.arcadeDrive(self.stick)

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
