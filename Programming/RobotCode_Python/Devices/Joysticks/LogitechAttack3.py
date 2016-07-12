import wpilib

class LogitechAttack3(wpilib.Joystick):

    AXIS_X = 'X'
    AXIS_Y = 'Y'
    AXIS_THROTTLE = 'Throttle'

    BUTTON_TRIGGER_1 = 'Trigger - 1'
    BUTTON_THUMB_2 = 'Thumb - 2'
    BUTTON_THUMB_3 = 'Thumb - 3'
    BUTTON_THUMB_4 = 'Thumb - 4'
    BUTTON_THUMB_5 = 'Thumb - 5'
    BUTTON_BOTTOM_6 = 'Bottom - 6'
    BUTTON_BOTTOM_7 = 'Bottom - 7'
    BUTTON_BOTTOM_8 = 'Bottom - 8'
    BUTTON_BOTTOM_9 = 'Bottom - 9'
    BUTTON_BOTTOM_10 = 'Bottom - 10'
    BUTTON_BOTTOM_11 = 'Bottom - 11'

    AXES = [AXIS_X,
            AXIS_Y,
            AXIS_THROTTLE
            ]

    BUTTONS = [BUTTON_TRIGGER_1,
               BUTTON_THUMB_2,
               BUTTON_THUMB_3,
               BUTTON_THUMB_4,
               BUTTON_THUMB_5,
               BUTTON_BOTTOM_6,
               BUTTON_BOTTOM_7,
               BUTTON_BOTTOM_8,
               BUTTON_BOTTOM_9,
               BUTTON_BOTTOM_10,
               BUTTON_BOTTOM_11
               ]

    def __init__(self, port):
        super().__init__(port, numAxisTypes=len(self.AXES), numButtonTypes=len(self.BUTTONS))

    def getAxisByName(self, name):
        if name in self.AXES:
            return super().getRawAxis(self.AXES.index(name))

    def getButtonByName(self, name):
        if name in self.BUTTONS:
            return super().getRawButton(self.BUTTONS.index(name))

    def get_x(self):
        return self.getAxisByName(self.AXIS_X)

    def get_y(self):
        return self.getAxisByName(self.AXIS_Y)

    def get_throttle(self):
        return self.getAxisByName(self.AXIS_THROTTLE)




