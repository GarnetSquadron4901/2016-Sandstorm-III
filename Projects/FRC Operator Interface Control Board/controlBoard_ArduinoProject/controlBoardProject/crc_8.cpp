// The 1-Wire CRC scheme is described in Maxim Application Note 27:
// "Understanding and Using Cyclic Redundancy Checks with Maxim iButton Products"

#include "crc_8.h"

uint8_t calculate_crc_8( char *addr, size_t len)
{
     uint8_t crc=0;
     
     for (uint8_t i=0; i<len;i++) 
     {
           uint8_t inbyte = (uint8_t) addr[i];
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
