import wpilib

class LogitechAttack3(wpilib.Joystick):
    AXES = ['X',
            'Y',
            'Throttle']
    BUTTONS = ['Trigger - 1',
               'Thumb - 2',
               'Thumb - 3',
               'Thumb - 4',
               'Thumb - 5',
               'Bottom - 6',
               'Bottom - 7',
               'Bottom - 8',
               ]

    def __init__(self, port):
        super().__init__(port, )
