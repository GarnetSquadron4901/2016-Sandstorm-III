#include <Servo.h>
#include <stdio.h>
#include <stdlib.h>
#include "hardwareMap.h"
#include "crc_8.h"

#define SERIAL_BAUD     250000
#define SERIAL_TIMEOUT  500
#define SERIAL_EOL      '\n'

#define SENSOR_OUT_STRING_LENGTH 256

#define VAL_STRING_LEN 8

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
  Serial.println("FRC Control Board");

}

void loop() 
{
//  Serial.println("Loop");
  uint8_t u8_bytesRead = 0;
  char sensorStringBuffer[SENSOR_OUT_STRING_LENGTH];
  memset(sensorStringBuffer, '\0', SENSOR_OUT_STRING_LENGTH);

  establishContact();
    
  // if we get a valid byte, read analog ins:
  do {
    u8_bytesRead = Serial.readBytesUntil(SERIAL_EOL, sensorStringBuffer, SENSOR_OUT_STRING_LENGTH);
    if(u8_bytesRead > 0) {
      processBuffer(sensorStringBuffer); 
      printSensorString();
    }
  } while (u8_bytesRead > 0);
}

void establishContact(void) {
  resetHardware(0); 
  setStatusLED(LOW);  

  while (Serial.available() == 0) {
    // Toggle the LED to indicate no connection
    toggleStatusLED();
    delay(1000);
  }
}

void printSensorString(void)
{
  uint8_t u8_crcVal;
  uint8_t u8_i;
  char sensorStringBuffer[SENSOR_OUT_STRING_LENGTH];
  uint8_t au8_ANA_values[NUM_OF_ANA_INS];
  uint8_t au8_SW_values[NUM_OF_SW_INS];
  char sz_value[VAL_STRING_LEN];

  // Clear contents of string
  memset(sensorStringBuffer, '\0', SENSOR_OUT_STRING_LENGTH);
  
  // Convert Switch Values to String
  strcat(sensorStringBuffer, "SW:");
  strcat(sensorStringBuffer, String(getSwitchMask(), HEX).c_str());
  strcat(sensorStringBuffer, ";");

  // Convert Analog Values to String
  getAnalogArray(au8_ANA_values, NUM_OF_ANA_INS);
  strcat(sensorStringBuffer, "ANA:");
  for(u8_i = 0; u8_i < NUM_OF_ANA_INS; u8_i++) {
    utoa(au8_ANA_values[u8_i], sz_value, VAL_STRING_LEN);
    strcat(sensorStringBuffer,  sz_value);
    
    if (u8_i < NUM_OF_ANA_INS-1)
      strcat(sensorStringBuffer, ",");
    else
      strcat(sensorStringBuffer, ";");
  }

  // Calculate CRC-8 on current string
  u8_crcVal = calculate_crc_8( sensorStringBuffer, (size_t) strlen(sensorStringBuffer) );

  // Print String
  Serial.print(sensorStringBuffer);
  // Print CRC
  Serial.print("CRC:");
  Serial.print(u8_crcVal);
  Serial.println(";");
  Serial.flush();
  
}

void processBuffer(char* sensorStringBuffer)
{ 
  uint8_t au8_LED_values[NUM_OF_LED_OUTS];
  uint8_t au8_PWM_values[NUM_OF_PWM_OUTS];
  char sz_LEDPWM[SENSOR_OUT_STRING_LENGTH];

  String str_sensorStringBuffer(sensorStringBuffer);
  uint8_t u8_CRC = (uint8_t) str_sensorStringBuffer.substring(str_sensorStringBuffer.indexOf("CRC:") + strlen("CRC:")).toInt();
  String str_Data = str_sensorStringBuffer.substring(0, str_sensorStringBuffer.indexOf("CRC:"));
  strncpy(sz_LEDPWM, str_Data.c_str(), SENSOR_OUT_STRING_LENGTH);
  
  // Check CRC-8
  if(u8_CRC == calculate_crc_8(sz_LEDPWM, str_Data.length()))
  {
   // Convert String to Values
   
   for(uint8_t u8_pwmIndex = 0; u8_pwmIndex < NUM_OF_PWM_OUTS; u8_pwmIndex++)
     au8_PWM_values[u8_pwmIndex] = 90;
     
   for(uint8_t u8_ledIndex = 0; u8_ledIndex < NUM_OF_LED_OUTS; u8_ledIndex++)
     au8_LED_values[u8_ledIndex] = 1;
   
   setLEDArray(au8_LED_values, NUM_OF_LED_OUTS);
   setPWMArray(au8_PWM_values, NUM_OF_PWM_OUTS);
   
   setStatusLED(HIGH);
  }
  else
    setStatusLED(LOW);
}
