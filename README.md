#2016 Robot Code - FIRST Robotics Team 4901 - Garnet Squadron

## Languages
- Robot - LabVIEW
- Dashboard - LabVIEW
- Vision Processing on Raspberry Pi
	- LED Control - Python
	- Vision Processing - Java using GRIP

## Features
- 8 drive modes
	- Arcade
	- Split Axis Arcade
	- Tank
	- Vision
	- Encoder Distance
	- Braked
	- Ultrasonic Distance
	- IMU Yaw Feedback
- Arm Control
	- PID
	- Preset Buttons
	- Manual arm control with closed-loop feedback from potentiometer
	- Automatic locking/unlocking with pneumatic cylinders
	- Automatic arm raising when driving faster than a preset speed
- Parameters - Most robot constants are parameterized to allow run-time changes to parameters such as arm angles, voltage to angle conversion, etc. 
- [Custom operator interface](https://github.com/GarnetSquardon4901/Operator-Interface-Control-Board)

## Checkout Process
To check out the Sand Storm III repository, simply download the [update.bat](https://github.com/GarnetSquardon4901/2016-Sand-Storm-III/raw/master/update.bat) and run it.

You'll need to install TortoiseSVN v1.8.x from [SourceForge](https://sourceforge.net/projects/tortoisesvn/files/). Newer versions (such as v1.9) don't work with the LabVIEW Plugin TSVN.

