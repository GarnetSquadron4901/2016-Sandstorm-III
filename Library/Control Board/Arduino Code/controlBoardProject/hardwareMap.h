#ifndef HARDWARE_MAP_H
#define HARDWARE_MAP_H

#include <Arduino.h>
#include <Servo.h>
#include <math.h>
#include <stdint.h>
#include <cstring.h>

// Defines how many inputs and outputs there are
#define NUM_OF_PWM_OUTS 11  // Number of PWM Outputs
#define NUM_OF_LED_OUTS 16  // Number of LED Outputs (through shift register)
#define NUM_OF_SW_INS   16  // Number of Switch Inputs
#define NUM_OF_ANA_INS  16  // Number of Analog Inputs

void initHardware(void); 
void resetHardware(uint8_t);
void updateHardware(void); 
void setStatusLED(uint8_t);
void toggleStatusLED(void); 

void setLED(uint8_t u8_ledNum, uint8_t u8_ledState);
void setPWM(uint8_t u8_pwmNum, uint8_t u8_pwmAngle);
uint8_t getAnalog(uint8_t u8_analogPin);
uint8_t getSwitch(uint8_t u8_switchPin); 

void setLEDArray(uint8_t *u8_ledStates, size_t arrayLength);
void setPWMArray(uint8_t *u8_pwmStates, size_t arrayLength);
void getAnalogArray(uint8_t *u8_analogValues, size_t arrayLength);
void getSwitchArray(uint8_t *u8_switchValues, size_t arrayLength);

#endif // HARDWARE_MAP_H
