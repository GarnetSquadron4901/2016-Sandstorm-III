
# Turn LEDs blue indicating that the process is starting
. /home/pi/start_led.sh

# Set LED parameters
python /home/pi/leds/set_error_color.py 255 0 0
python /home/pi/leds/set_load_color.py 0 255 0
python /home/pi/leds/set_completed_color.py 0 255 0
python /home/pi/leds/set_running_color.py 0 255 255
sudo python /home/pi/leds/set_progress.py 0
python /home/pi/leds/run.py


while ! sudo ping -c 1 -n roborio-4901-frc.local; do sleep 1; done

sleep 5

python /home/pi/leds/set_progress.py 33

# Start mjpg_streamer
. /home/pi/start_mjpg.sh
sleep 5

if (ps | grep mjpg_streamer); then 
	python /home/pi/leds/set_progress.py 67
else
	# Error starting mjpg streame
	python /home/pi/leds/set_error.py
	exit
fi

. /home/pi/start_grip.sh
sleep 5

if (ps | grep java); then
	python /home/pi/leds/set_progress.py 100
else
	# Error starting mjpg streamer
	python /home/pi/leds/set_error.py
	exit
fi




