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

void blankLEDs(void);
void setLED(uint8_t, uint8_t);
void setPWM(uint8_t, uint8_t);
uint8_t getAnalog(uint8_t);

void setLEDs(uint16_t);
void setPWMArray(uint8_t*, size_t);
void getAnalogArray(uint8_t*, size_t);
uint16_t getSwitchMask(void);

#endif // HARDWARE_MAP_H
