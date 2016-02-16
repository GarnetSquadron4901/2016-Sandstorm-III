#include <Servo.h>
#include <stdio.h>
#include <stdlib.h>
#include "hardwareMap.h"
#include "crc_8.h"
#include <SoftwareSerial.h>

#define SERIAL_BAUD     115200
#define SERIAL_TIMEOUT  500
#define SERIAL_EOL      '\n'

#define SENSOR_OUT_STRING_LENGTH 256

#define VAL_STRING_LEN 8

#define DEBUG

bool debugEnabled = false;

#ifdef DEBUG
SoftwareSerial debugSerial(50, 52); // RX, TX
#endif 

typedef enum {
  CRC_ERROR = -1,
  CRC_OK    = 0
} CRC_Status; 

// Variable Declarations
void establishConnection(void);
void printSensorString(void); 
void processBuffer(char*);


void setup()
{
  Serial.begin(SERIAL_BAUD);
  Serial.setTimeout(SERIAL_TIMEOUT); 
  Serial.println("FRC Control Board");

  #ifdef DEBUG
  debugSerial.begin(115200);
  debugSerial.setTimeout(SERIAL_TIMEOUT);
  debugSerial.listen();
  debugSerial.println("FRC Control Board");
  #endif
  
  initHardware(); 
}

void loop() 
{
//  Serial.println("Loop");
  uint8_t u8_bytesRead = 0;
  char sensorStringBuffer[SENSOR_OUT_STRING_LENGTH];

  establishConnection();
    
  // if we get a valid byte, read analog ins:
  do {
    memset(sensorStringBuffer, '\0', SENSOR_OUT_STRING_LENGTH);
    u8_bytesRead = Serial.readBytesUntil(SERIAL_EOL, sensorStringBuffer, SENSOR_OUT_STRING_LENGTH);
    if(u8_bytesRead > 0) {
      processBuffer(sensorStringBuffer); 
      printSensorString();
    }
  } while (u8_bytesRead > 0);
}

void establishConnection(void) {
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
  strcat(sensorStringBuffer, "ANA:");
  for(u8_i = 0; u8_i < NUM_OF_ANA_INS; u8_i++) {
    utoa(getAnalog(u8_i), sz_value, 10);
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
  char sz_PWM[SENSOR_OUT_STRING_LENGTH];
  char* pch;

  String str_sensorStringBuffer(sensorStringBuffer);
  uint8_t u8_CRC = (uint8_t) str_sensorStringBuffer.substring(str_sensorStringBuffer.indexOf("CRC:") + strlen("CRC:")).toInt();
  String str_Data = str_sensorStringBuffer.substring(0, str_sensorStringBuffer.indexOf("CRC:"));
  
  // Check CRC-8
  if(u8_CRC == calculate_crc_8((char*)str_Data.c_str(), str_Data.length())) {
   
   // Parse LEDs
   setLEDs((uint16_t)str_Data.substring(str_Data.indexOf("LED:") + strlen("LED:"), str_Data.indexOf(";")).toInt());

    // Parse PWMs
    memset(sz_PWM, '\0', SENSOR_OUT_STRING_LENGTH);
    strncpy(sz_PWM, str_Data.substring(str_Data.indexOf("PWM:") + strlen("PWM:")).c_str(), SENSOR_OUT_STRING_LENGTH);
    pch = strtok(sz_PWM, ",");
    uint8_t u8_pwmIndex = 0;
    while(pch != NULL && u8_pwmIndex < NUM_OF_PWM_OUTS) {
      setPWM(u8_pwmIndex, (uint8_t) atoi(pch));
      pch = strtok(NULL, ",");
      u8_pwmIndex++;
    }
   setStatusLED(HIGH);
  }
  else {
    
    setStatusLED(LOW);
  }
}
