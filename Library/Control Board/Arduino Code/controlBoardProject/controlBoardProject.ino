#include <Servo.h>
#include <stdio.h>
#include <cstring.h>
#include "hardwareMap.h"

#define Serial_BAUD     115200
#define Serial_TIMEOUT  1000
#define Serial_EOL      '\n'
#define ESTABLISH_RATE  500

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
  Serial.begin(115200); 
  Serial.begin(Serial_BAUD);
  Serial.setTimeout(Serial_TIMEOUT); 

}

void loop() 
{
  char SerialBuffer[SENSOR_OUT_STRING_LENGTH];
  
  memset(SerialBuffer, 0, SENSOR_OUT_STRING_LENGTH); 
  
  // if we get a valid byte, read analog ins:
  if(Serial.readBytesUntil(Serial_EOL, SerialBuffer, SENSOR_OUT_STRING_LENGTH) > 0)
  {
    processBuffer(SerialBuffer); 
    //Serial.println(SerialBuffer); 
    updateHardware();
    printSensorString();
  }
  else // Timeout occured
    establishContact();

}

void establishContact(void) 
{
  resetHardware(0); 
  setStatusLED(LOW); 
 uint32_t u32_timerValue;

  u32_timerValue = millis() + ESTABLISH_RATE;  
  while (Serial.available() <= 0) 
  {
    if(millis() >= u32_timerValue)
    {
      // Send data string to the computer
      printSensorString(); 
      // Toggle the LED to indicate no connection
      toggleStatusLED();
      u32_timerValue = millis() + ESTABLISH_RATE; 
    }
  }
}

void printSensorString(void)
{
  uint8_t au8_ANA_values[NUM_OF_ANA_INS];
  uint8_t au8_SW_values[NUM_OF_SW_INS]; 
  uint8_t u8_crc;
  char sz_dataOut[SENSOR_OUT_STRING_LENGTH]; 
  
  memset(sz_dataOut, 0, SENSOR_OUT_STRING_LENGTH); 
  
  getAnalogArray(au8_ANA_values, NUM_OF_ANA_INS);
  getSwitchArray(au8_SW_values, NUM_OF_SW_INS);
  
   // Convert Values to String
  sprintf(sz_dataOut, "SW: %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d; ANA: %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d;",
  au8_SW_values[0],  au8_SW_values[1],  au8_SW_values[2],   au8_SW_values[3],   au8_SW_values[4],   au8_SW_values[5],   au8_SW_values[6],   au8_SW_values[7],
  au8_SW_values[8],  au8_SW_values[9],  au8_SW_values[10],  au8_SW_values[11],  au8_SW_values[12],  au8_SW_values[13],  au8_SW_values[14],  au8_SW_values[15],
  au8_ANA_values[0], au8_ANA_values[1], au8_ANA_values[2],  au8_ANA_values[3],  au8_ANA_values[4],  au8_ANA_values[5],  au8_ANA_values[6],  au8_ANA_values[7], 
  au8_ANA_values[8], au8_ANA_values[9], au8_ANA_values[10], au8_ANA_values[11], au8_ANA_values[12], au8_ANA_values[13], au8_ANA_values[14], au8_ANA_values[15]);
  
  // Calculate CRC-8 (CCITT)
  u8_crc = crc8((uint8_t*)sz_dataOut, strlen(sz_dataOut));
  
  Serial.print(sz_dataOut);
  Serial.print(" CRC: "); 
  Serial.print(u8_crc);
  Serial.print('\n');
  
  // Print String with CRC-8 attached
  
}

uint32_t u32_crcFailures = 0; 

void processBuffer(char* SerialBuffer)
{
  
  CRC_Status e_crcCheck = CRC_OK; 
  uint8_t au8_LED_values[NUM_OF_LED_OUTS];
  uint8_t au8_PWM_values[NUM_OF_PWM_OUTS];
  uint8_t u8_dataLength;
  uint8_t u8_crcValueIn; 
  uint8_t u8_crcValueComputed; 
 
  char sz_dataIn[SENSOR_OUT_STRING_LENGTH];
  memset(sz_dataIn, 0, SENSOR_OUT_STRING_LENGTH);
  char sz_CRCIn[SENSOR_OUT_STRING_LENGTH];   
  memset(sz_CRCIn, 0, SENSOR_OUT_STRING_LENGTH);
  
  char * pch;
  
  pch = strrchr(SerialBuffer, ';');
  if(pch)
  {
    
    
    u8_dataLength =  pch - SerialBuffer + 1; 
    
    // Copy Data
    memcpy(sz_dataIn, SerialBuffer, u8_dataLength); 
    strcpy(sz_CRCIn, SerialBuffer + u8_dataLength); 
    
    sscanf(sz_CRCIn, "%*s %d", &u8_crcValueIn); 
    
    // Calculate CRC
    u8_crcValueComputed = crc8((uint8_t*)SerialBuffer, u8_dataLength);

    // Check CRC Results
    if(u8_crcValueIn == u8_crcValueComputed)
      e_crcCheck = CRC_OK;
    else
      e_crcCheck = CRC_ERROR; 
  
    // Check CRC-8
    if(e_crcCheck == CRC_OK)
    {
     // Convert String to Values
     pch = strtok(sz_dataIn, " ");  // Trash LEDs
     for(uint8_t u8_ledIndex = 0; u8_ledIndex < NUM_OF_LED_OUTS; u8_ledIndex++)
     {
       pch = strtok(NULL, " ");
       au8_LED_values[u8_ledIndex] = atoi(pch); 
     }
     pch = strtok(NULL, " ");  // Trash PWMs
     for(uint8_t u8_pwmIndex = 0; u8_pwmIndex < NUM_OF_PWM_OUTS; u8_pwmIndex++)
     {
       pch = strtok(NULL, " "); 
       au8_PWM_values[u8_pwmIndex] = atoi(pch);
     }
     // Set Values to the hardware
     setLEDArray(au8_LED_values, NUM_OF_LED_OUTS);
     setPWMArray(au8_PWM_values, NUM_OF_PWM_OUTS);
     setStatusLED(HIGH);
    }
    else
    {
      setStatusLED(LOW); 
    }
  }
  else
    setStatusLED(LOW);
}

// The 1-Wire CRC scheme is described in Maxim Application Note 27:
// "Understanding and Using Cyclic Redundancy Checks with Maxim iButton Products"

uint8_t crc8( uint8_t *addr, uint8_t len)
{
      uint8_t crc=0;
      
      for (uint8_t i=0; i<len;i++) 
      {
            uint8_t inbyte = addr[i];
            for (uint8_t j=0;j<8;j++) 
            {
                  uint8_t mix = (crc ^ inbyte) & 0x01;
                  crc >>= 1;
                  if (mix) 
                        crc ^= 0x8C;
                  
                  inbyte >>= 1;
            }
      }
      return crc;
}
