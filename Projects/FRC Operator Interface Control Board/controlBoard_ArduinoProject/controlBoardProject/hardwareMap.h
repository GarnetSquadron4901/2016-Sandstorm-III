#ifndef HARDWARE_MAP_H
#define HARDWARE_MAP_H

#include <Arduino.h>
#include <Servo.h>
#include <math.h>
#include <stdint.h>

// Defines how many inputs and outputs there are
#define NUM_OF_PWM_OUTS 11  // Number of PWM Outputs
#define NUM_OF_LED_OUTS 16  // Number of LED Outputs (through shift register)
#define NUM_OF_SW_INS   16  // Number of Switch Inputs
#define NUM_OF_ANA_INS  16  // Number of Analog Inputs

void initHardware(void); 
void resetHardware(uint8_t);
void setStatusLED(uint8_t);
void toggleStatusLED(void); 

void setLED(uint8_t u8_ledNum, uint8_t u8_ledState);
void setPWM(uint8_t u8_pwmNum, uint8_t u8_pwmAngle);
uint8_t getAnalog(uint8_t u8_analogPin);

void setLEDArray(uint8_t *u8_ledStates, size_t arrayLength);
void setPWMArray(uint8_t *u8_pwmStates, size_t arrayLength);
void getAnalogArray(uint8_t *u8_analogValues, size_t arrayLength);
uint16_t getSwitchMask(void);

#endif // HARDWARE_MAP_H
