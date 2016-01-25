#include "hardwareMap.h"

// Settings for how fast and how precise the servo sweeps.
// The full sweep time should be very close to SWEEP_COUNT * SWEEP_DELAY
#define SWEEP_COUNT 200.0  // Number of iterations to step the servo
#define SWEEP_DELAY 10     // Delay between steps (ms)

// How far to sweep the servo from 0 to SWEEP_FULL_SCALE degrees
#define SWEEP_FULL_SCALE 180.0

// Pulse width adjustments for non-compliant servos (defaults: PWM_MIN = 544; PWM_MAX = 2400)
#define PWM_MIN 600
#define PWM_MAX 2400

// The analog pin map is based on the Arduino Mega 2560 pins.
// Analog Pin Map:               {ANA0, ANA1, ANA2, ANA3, ANA4, ANA5, ANA6, ANA7, ANA8, ANA9, ANA10, ANA11, ANA12, ANAN13, ANA14, ANA15}
const uint8_t u8_Analog_Pins[] = {69,   68,   67,   66,   65,   64,   63,   62,   61,   60,   59,    58,    57,    56,     55,    54   }; 

// PWM Pin Map:                  {PWM0, PWM1, PWM2, PWM3, PWM4, PWM5, PWM6, PWM7, PWM8, PWM9, PWM10}
const uint8_t u8_PWM_Pins[] =    {4,    5,    2,    3,    6,    7,    8,    9,    10,   11,   12   }; 

// Switch Pin Map:               {SW0, SW1, SW2, SW3, SW4, SW5, SW6, SW7, SW8, SW9, SW10, SW11, SW12, SW13, SW14, SW15}
const uint8_t u8_SW_Pins[] =     {37,  36,  35,  34,  33,  32,  31,  30,  29,  28,  27,   26,   25,   24,   23,   22  }; 

// LED Shift Register Pins
enum {
  LED_ShiftReg_LAT   = 38,  // Latch pin -  The data in the 16-bit shift register continue to transfer to the output on/off data latch while LAT is high.
  LED_ShiftReg_BLANK = 39,  // Blank pin - Blank, all outputs.
  LED_ShiftReg_SIN   = 40,  // Shifted Data In - Serial data input for driver on/off control.
  LED_ShiftReg_SCLK  = 41   // Shifter Clock In - Serial data shift clock.
};

// Status LED
enum {
  STATUS_LED = 13
};


// Global Variables
uint8_t u8_StatusLED_value; 
Servo servoOutputs[NUM_OF_PWM_OUTS];

// Sets the Status LED to on or off. 
void setStatusLED(uint8_t u8_value)
{
  u8_StatusLED_value = u8_value;
  digitalWrite(STATUS_LED, u8_StatusLED_value);   
}

// Toggles the Status LED (Blinks)
void toggleStatusLED(void)
{
   setStatusLED(!u8_StatusLED_value);
}

// Initializes hardware by setting up the hardware pins and doing a self-test
void initHardware(void)
{
  // Analog Configuration
  analogReference(DEFAULT);
  uint8_t u8_Analog_Index;
  for(u8_Analog_Index = 0; u8_Analog_Index < NUM_OF_ANA_INS; u8_Analog_Index++)
    pinMode(u8_Analog_Pins[u8_Analog_Index], INPUT);
    
  // Switch Configuration
  uint8_t u8_Switch_Index;
  for(u8_Switch_Index = 0; u8_Switch_Index < NUM_OF_SW_INS; u8_Switch_Index++)
    pinMode(u8_SW_Pins[u8_Switch_Index], INPUT_PULLUP);
    
  // PWM Configuration
  uint8_t u8_PWM_Index;
  for(u8_PWM_Index = 0; u8_PWM_Index < NUM_OF_PWM_OUTS; u8_PWM_Index++)
  {
    // Set the pinmode to output
    pinMode(u8_PWM_Pins[u8_PWM_Index], OUTPUT);
    // Attach the servo to the PWM generator
    servoOutputs[u8_PWM_Index].attach(u8_PWM_Pins[u8_PWM_Index], PWM_MIN, PWM_MAX);
  }
    
  // LED Shift Register Configuration
  pinMode(LED_ShiftReg_LAT,   OUTPUT);
  pinMode(LED_ShiftReg_BLANK, OUTPUT);
  pinMode(LED_ShiftReg_SIN,   OUTPUT);
  pinMode(LED_ShiftReg_SCLK,  OUTPUT);
  blankLEDs();
  
  // Status LED Configuration
  pinMode(STATUS_LED,         OUTPUT); 
  
  // Initialize Values and perform self-test
  resetHardware(0); 
}

void blankLEDs(void) {
  digitalWrite(LED_ShiftReg_BLANK, HIGH);
  delayMicroseconds(1);
  digitalWrite(LED_ShiftReg_BLANK, LOW);
}

// Sets all the LEDs in the LED values array.
void setLEDs(uint16_t u16_ledMask) {
  digitalWrite(LED_ShiftReg_LAT, LOW);
  for (uint8_t u8_i = 0; u8_i < 16; u8_i++) {
    digitalWrite(LED_ShiftReg_SIN, (u16_ledMask & 0x8000) ? HIGH:LOW);
    digitalWrite(LED_ShiftReg_SCLK, HIGH);
    delayMicroseconds(1);
    digitalWrite(LED_ShiftReg_SCLK, LOW);
    u16_ledMask <<= 1;
  }
  digitalWrite(LED_ShiftReg_LAT, HIGH);
}

// Read the switch values into au8_SW_values[].
uint16_t getSwitchMask(void)
{
  uint8_t u8_Switch_Index = NUM_OF_SW_INS;
  uint16_t u16_SW_values = (digitalRead(u8_SW_Pins[u8_Switch_Index--])? 0x0000:0x0001);
  do {
    u16_SW_values <<= 1;
    u16_SW_values |= (digitalRead(u8_SW_Pins[u8_Switch_Index])? 0x0000:0x0001);
  } while(u8_Switch_Index-- != 0);
  return u16_SW_values;
}

uint8_t getAnalog(uint8_t u8_AnalogChannel) {
  if(u8_AnalogChannel < NUM_OF_ANA_INS)
    return analogRead(u8_Analog_Pins[u8_AnalogChannel]) >> 2;
}


// Sets the LED outputs off and returns the servos back to 0 degrees. 
void resetHardware(uint8_t u8_selfTest)
{
  // Set LEDs off
  setLEDs(0x0000);
  
  // Turn Status LED off
  setStatusLED(LOW);
  
  // Set Servos to 0 (account for any floating point error, as the sweep should return them back to 0). 
  for(uint8_t u8_PWM_Index = 0; u8_PWM_Index < NUM_OF_PWM_OUTS; u8_PWM_Index++)
      setPWM(u8_PWM_Index, 0); 
}

void setPWM(uint8_t u8_pwmChannel, uint8_t u8_pwmValue) {
  if(u8_pwmChannel < NUM_OF_PWM_OUTS)
    servoOutputs[u8_pwmChannel].write(u8_pwmValue);
}


