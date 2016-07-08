import wpilib


class Generic_Controller:
    """ This class is the parent class all controllers """
    def __init__(self, channel_descriptions):
        self.channel_descriptions = channel_descriptions

        # Create an empty registry to store all the I/O in
        self.registry = {}
        for key in self.channel_descriptions.keys():
            self.registry.update({key: {}})

    def _add_channel_to_registry(self, type, name, channel):
        self._assert_channel_valid(type, channel)
        self.registry[type].update({channel: name})

    def _assert_channel_valid(self, channel_type, channel):
        assert channel_type in self.channel_descriptions.keys(), "Type %s is not a valid type." % channel_type
        assert channel in self.channel_descriptions[channel_type], 'Channel %d out of range for %s type.' % \
                                                                     (channel, channel_type)
        assert channel not in self.registry[channel_type], 'Channel %d is already in use by %s' % \
                                                               (channel, self.registry[channel_type][channel])

    def add_digital_output(self, name, channel, return_type=wpilib.DigitalOutput):
        self._add_channel_to_registry(self.DIO_NAME, name, channel)
        if return_type is not None:
            return return_type(channel=channel)

    def add_digital_input(self, name, channel, return_type=wpilib.DigitalInput):
        self._add_channel_to_registry(self.DIO_NAME, name, channel)
        if return_type is not None:
            return return_type(channel=channel)

    def add_analog_input(self, name, channel, return_type=wpilib.AnalogInput):
        self._add_channel_to_registry(self.ANALOG_NAME, name, channel)
        if return_type is not None:
            return return_type(channel=channel)

    def add_pwm_output(self, name, channel, return_type=wpilib.PWM):
        self._add_channel_to_registry(self.PWM_NAME, name, channel)
        if return_type is not None:
            return return_type(channel=channel)

    def add_relay_output(self, name, channel, direction=wpilib.Relay.Direction.kBoth, return_type=wpilib.Relay):
        self._add_channel_to_registry(self.RELAY_NAME, name, channel)
        if return_type is not None:
            return return_type(channel=channel, direction=direction)

class RoboRIO_Controller(Generic_Controller):
    """ This class provides the RoboRIO Inputs and Outputs.

    The specifications for the RoboRIO can be found at the following web address:
    # https://decibel.ni.com/content/docs/DOC-30419

    """
    DIO_NAME = 'Digital'
    DIO_CHANNELS = range(16)

    ANALOG_NAME = 'Analog'
    ANA_CHANNELS = range(4)

    PWM_NAME = 'PWM'
    PWM_CHANNELS = range(10)

    RELAY_NAME = 'Relay'
    RELAY_CHANNELS = range(4)

    SPI_NAME = 'SPI'
    SPI_CS_PINS = range(4)

    I2C_NAME = 'I2C'
    I2C_ADDRESSES = range(128)

    CHANNEL_DESCRIPTIONS = {DIO_NAME: DIO_CHANNELS,
                            ANALOG_NAME: ANA_CHANNELS,
                            PWM_NAME: PWM_CHANNELS,
                            RELAY_NAME: RELAY_CHANNELS,
                            SPI_NAME: SPI_CS_PINS,
                            I2C_NAME: I2C_ADDRESSES}

    def __init__(self):
        super(RoboRIO_Controller, self).__init__(self.CHANNEL_DESCRIPTIONS)



