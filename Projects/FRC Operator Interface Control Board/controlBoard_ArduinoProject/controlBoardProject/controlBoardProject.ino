#include <Servo.h>
#include <stdio.h>
#include <cstring.h>
#include "hardwareMap.h"

#define SERIAL_BAUD     115200
#define SERIAL_TIMEOUT  1000
#define SERIAL_EOL      '\n'

#define SENSOR_OUT_STRING_LENGTH 256

typedef enum {
  CRC_ERROR = -1,
  CRC_OK    = 0
} CRC_Status; 

// Variable Declarations
void establishContact(void);
void printSensorString(void); 
void processBuffer(char*);


void setup()
{
  initHardware(); 
  Serial.begin(SERIAL_BAUD);
  Serial.setTimeout(SERIAL_TIMEOUT); 

}

void loop() 
{
  char serialBuffer[SENSOR_OUT_STRING_LENGTH];
  
  // if we get a valid byte, read analog ins:
  if(Serial.readBytesUntil(SERIAL_EOL, serialBuffer, SENSOR_OUT_STRING_LENGTH) > 0)
    processBuffer(serialBuffer); 
  else // Timeout occured
    establishContact();

}

void establishContact(void) 
{
  resetHardware(0); 
  setStatusLED(LOW);  while (Serial.available() <= 0) 
  {
    // Send data string to the computer
    printSensorString(); 
    // Toggle the LED to indicate no connection
    toggleStatusLED();
    delay(500);
  }
  // Reset Servos and LEDs
  resetHardware(1);
}

void printSensorString(void)
{
  uint8_t au8_ANA_values[NUM_OF_ANA_INS];
  uint8_t au8_SW_values[NUM_OF_SW_INS]; 
  
  getAnalogArray(au8_ANA_values, NUM_OF_ANA_INS);
  getSwitchArray(au8_SW_values, NUM_OF_SW_INS);
  
  // Convert Values to String
  
  // Calculate CRC-8
  
  // Print String with CRC-8 attached
  
}

void processBuffer(char* serialBuffer)
{
  CRC_Status e_crcCheck = CRC_OK; 
  uint8_t au8_LED_values[NUM_OF_LED_OUTS];
  uint8_t au8_PWM_values[NUM_OF_PWM_OUTS];

  
  // Check CRC-8
  if(e_crcCheck == CRC_OK)
  {
   // Convert String to Values
   
   for(uint8_t u8_pwmIndex = 0; u8_pwmIndex < NUM_OF_PWM_OUTS; u8_pwmIndex++)
     au8_PWM_values[u8_pwmIndex] = 90;
     
   for(uint8_t u8_ledIndex = 0; u8_ledIndex < NUM_OF_LED_OUTS; u8_ledIndex++)
     au8_LED_values[u8_ledIndex] = 1;
   
   setLEDArray(au8_LED_values, NUM_OF_LED_OUTS);
   setPWMArray(au8_PWM_values, NUM_OF_PWM_OUTS);
   updateHardware();
   setStatusLED(HIGH);
  }
  else
    setStatusLED(LOW);
}
