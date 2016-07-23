from threading import Timer
import wpilib

class PerpetualTimer:

    def __init__(self, t, hFunction):
        self.t=t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        try:
            self.hFunction()
        except Exception as e:
            print ('Could not run handle function: %s' % str(e))

        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

    def set_refresh_time(self, refresh_time):
        self.cancel()
        self.thread.interval = refresh_time
        self.start()
