# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import sys
import math
import Pyro4
import threading

from neopixel import *

# LED strip configuration:
LED_COUNT      = 24      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

class LED_Server(object):
	
	
	def __init__(self):

		# Create NeoPixel object with appropriate configuration.
		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
		# Intialize the library (must be called once before other functions).
		self.strip.begin()
		
		self.progress = 0
		
		self.completedColorR = 0
		self.completedColorG = 0
		self.completedColorB = 255
		
		self.runningColorR = 255
		self.runningColorG = 0
		self.runningColorB = 255
		
		self.loadingColorR = 0
		self.loadingColorG = 0
		self.loadingColorB = 255
		
		self.errorColorR = 255
		self.errorColorG = 0
		self.errorColorB = 0
		
		self.thread = threading.Thread(target=self.service)
		
		self.leds_off()
		
	def run(self):
		self.error = False
		self.run = True
		self.thread.start()

	def stop(self):
		self.run = False
		self.leds_off()
		
	def setProgress(self, _progress):
		self.progress = _progress
		
	def setRunningColor(self, r, g, b):
		self.runningColorR = r
		self.runningColorG = g
		self.runningColorB = b
		
	def setLoadingColor(self, r, g, b):
		self.loadingColorR = r
		self.loadingColorG = g
		self.loadingColorB = b
		
	def setCompletedColor(self, r, g, b):
		self.completedColorR = r
		self.completedColorG = g
		self.completedColorB = b
		
	def setErrorColor(self, r, g, b):
		self.errorColorR = r
		self.errorColorG = g
		self.errorColorB = b
		
	def setError(self):
		self.error = True
		
	def leds_off(self):
		for led in range(LED_COUNT):
			self.strip.setPixelColor(led, Color(0, 0, 0))
		self.strip.show()
		
	def service(self):
		i = 0
		while self.run == True:
			if self.error:
				for led in range(LED_COUNT):
						self.strip.setPixelColor(led, Color(self.errorColorR, self.errorColorG, self.errorColorB))
				self.strip.show()
				time.sleep(0.5)
			
			else:
		
				if self.progress < 100:
					completed = int(LED_COUNT * (float(self.progress) / 100.0))
					
					if i >= 100:
						i = 0
					else:
						i += 1
						
					for led in range (completed):
						self.strip.setPixelColor(led, Color(self.completedColorR, self.completedColorG, self.completedColorB))
					for led in range(completed, LED_COUNT):
						gain = (math.sin((i / 100.0) * 6.28 ) + 1.0) / 2.0
						self.strip.setPixelColor(led, Color(int(self.loadingColorR * gain), int(self.loadingColorG * gain), int(self.loadingColorB * gain)))
					self.strip.show()
					time.sleep(0.01)
				
				else:
					
					for led in range(LED_COUNT):
						self.strip.setPixelColor(led, Color(self.runningColorR, self.runningColorG, self.runningColorB))
					self.strip.show()
					time.sleep(0.5)


if __name__ == "__main__":
	ledService = LED_Server()
	daemon = Pyro4.Daemon()
	ns = Pyro4.locateNS()
	uri = daemon.register(ledService)
	ns.register('ledService', uri)
	print 'Ready'
	daemon.requestLoop()


