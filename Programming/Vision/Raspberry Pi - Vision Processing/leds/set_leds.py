# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import sys

from neopixel import *


# LED strip configuration:
LED_COUNT      = 24      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

if len(sys.argv) != 4:
	print 'Usage set_leds.py rrr ggg bbb - 8-bit'
	exit()
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()
stripColor = Color(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
for i in range (LED_COUNT):
	strip.setPixelColor( i, stripColor)
strip.show()
