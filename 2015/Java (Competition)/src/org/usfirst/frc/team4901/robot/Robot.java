
package org.usfirst.frc.team4901.robot;

import edu.wpi.first.wpilibj.*;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

/**
 * The VM is configured to automatically run this class, and to call the
 * functions corresponding to each mode, as described in the IterativeRobot
 * documentation. If you change the name of this class or the package after
 * creating this project, you must also update the manifest file in the resource
 * directory.
 */
public class Robot extends IterativeRobot {
	
	SmartDashboard smart;
	
	Joystick Joy1 = new Joystick(1);
	
	Talon LeftDriveA = new Talon(0);
	Talon LeftDriveB = new Talon(1);
	Talon RightDriveA = new Talon(2);
	Talon RightDriveB = new Talon(3);
	
	Talon StrafeWheel = new Talon(4);
	
	double Leftpower, Rightpower, Strafepower, moveValue, rotateValue;
	
	final double DEADBAND_THRESHOLD = 0.10;
	
	public void Forward(double mseconds, double power){

		for(int i = 0; i < mseconds; i++){
			LeftDriveA.set(power);
			LeftDriveB.set(power);
			RightDriveA.set(power);
			RightDriveB.set(power);
		}
		
		LeftDriveA.set(0);
		LeftDriveB.set(0);
		RightDriveA.set(0);
		RightDriveB.set(0);	
	}
	
	public double filterAxisDeadband (double val) {
		if (Math.abs(val) > DEADBAND_THRESHOLD) {
			return scale(val);
		}
		
		return 0;
	}
	
	public double scale (double val) {
		return val;
	}
	
	public void DriveControl(){
		LeftDriveA.set(Leftpower);
		LeftDriveB.set(Leftpower);
		RightDriveA.set(Rightpower);
		RightDriveB.set(Rightpower);
		StrafeWheel.set(Strafepower);
	}
	
	public void JoystickControl(){
		moveValue = -1 * filterAxisDeadband(Joy1.getRawAxis(1));
		rotateValue = -1 * filterAxisDeadband(Joy1.getRawAxis(4));
		Strafepower = filterAxisDeadband(Joy1.getRawAxis(3)) + (-filterAxisDeadband(Joy1.getRawAxis(2)));
		SmartDashboard.putNumber("move Value", moveValue);
		SmartDashboard.putNumber("rotate Value", rotateValue);
		SmartDashboard.putNumber("Strafe power", Strafepower);
	}
	
	public void CustomArcControl(){
        if (moveValue > 0.0) {
            if (rotateValue > 0.0) {
            	Leftpower = moveValue - rotateValue;
            	Rightpower = Math.max(moveValue, rotateValue);
            } else {
            	Leftpower = Math.max(moveValue, -rotateValue);
            	Rightpower = moveValue + rotateValue;
            }
        } else {
            if (rotateValue > 0.0) {
            	Leftpower = -Math.max(-moveValue, rotateValue);
            	Rightpower = moveValue + rotateValue;
            } else {
            	Leftpower = moveValue - rotateValue;
            	Rightpower = -Math.max(-moveValue, -rotateValue);
            }
        }			
	}
	
    /**
     * This function is run when the robot is first started up and should be
     * used for any initialization code.
     */
    public void robotInit() {
    	Leftpower = 0;
    	Rightpower = 0;
    }

    /**
     * This function is called periodically during autonomous
     */
    public void autonomousPeriodic() {
    	
    	Forward(200, 1);

    }

    /**
     * This function is called periodically during operator control
     */
    public void teleopPeriodic() {
        JoystickControl();
        CustomArcControl();
        DriveControl();        
    }
    
    /**
     * This function is called periodically during test mode
     */
    public void testPeriodic() {
    
    }
    
}
