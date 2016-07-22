import time

class PID_Base:
    def __init__(self, **kwargs):
        self.Kp = kwargs.get('Kp', 0.0)
        self.Ki = kwargs.get('Ki', 0.0)
        self.Kd = kwargs.get('Kd', 0.0)
        self.o_max = kwargs.get('output_max', 1)
        self.o_min = kwargs.get('output_min', -1)
        self.i_max = kwargs.get('integrator_max', 1)
        self.i_min = kwargs.get('integrator_min', -1)
        self.integrator = 0.0
        self.output = 0.0
        self.error = 0.0
        self.processvar = 0.0
        self.setpoint = 0.0
        self.old_update_time = None
        self.new_update_time = None
        self.dT = self.calc_dt()

    def get_output(self):
        return self.coerce(self.output, self.o_min, self.o_max)

    @staticmethod
    def coerce(value, min_val, max_val):
        if min_val > max_val:
            raise ArithmeticError('Maximum must be greater than minimum.')
        return  min(max(value, min_val), max_val)

    def set_setpoint(self, value):
        self.setpoint = value

    def set_processvar(self, value):
        self.processvar = value

    def get_gains(self):
        return self.Kp, self.Ki, self.Kd

    def set_gains(self, Kp, Ki, Kd):
        old = self.get_gains()
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        if old != self.get_gains():
            self.reset()

    def get_output_limits(self):
        return self.o_min, self.o_max

    def set_output_limits(self, o_min, o_max):
        if o_min > o_max:
            raise ArithmeticError('Maximum must be greater than minimum.')
        old = self.get_output_limits()
        self.o_min = o_min
        self.o_max = o_max
        if old != self.get_output_limits():
            self.reset()

    def get_integrator_limits(self):
        return self.i_min, self.i_max

    def set_integrator_limits(self, i_min, i_max):
        if i_min > i_max:
            raise ArithmeticError('Maximum must be greater than minimum.')
        old = self.get_integrator_limits()
        self.i_min = i_min
        self.i_max = i_max
        if old != self.get_integrator_limits():
            self.reset()

    def calc_dt(self):
        if self.old_update_time is None or self.new_update_time is None:
            self.dT = 0.0

        if self.new_update_time is not None:
            self.old_update_time = self.new_update_time
        else:
            self.old_update_time = time.time()
        self.new_update_time = time.time()
        self.dT = self.new_update_time - self.old_update_time
        return self.dT

    def calc_error(self):
        self.error = self.setpoint - self.processvar
        return self.error

    def calc_P(self, error=None):
        if error is None:
            error = self.error
        return self.Kp * error

    def calc_I(self, error=None):
        if error is None:
            error = self.error
        self.integrator = self.coerce((error * self.Ki) + self.integrator, self.i_min, self.i_max)
        return self.integrator

    def calc_D(self, error=None):
        if error is None:
            error = self.error
        return ((error - self.last_error) / self.dT) * self.Kd

    def reset(self):
        self.output = 0.0
        self.integrator = 0.0
        self.error = 0.0
        self.processvar = 0.0
        self.setpoint = 0.0
        self.old_update_time = time.time()
        self.new_update_time = self.old_update_time


class PID_Position(PID_Base):

    def update(self, process_var=None):
        if process_var is not None:
            self.set_processvar(process_var)
        self.calc_dt()
        self.calc_error()
        p = self.calc_P()
        i = self.calc_I()
        d = self.calc_D()
        self.output = self.coerce(p + i + d, self.o_min, self.o_max)

        return self.output()


class PID_Speed(PID_Base):

    def update(self, process_var=None):
        if process_var is not None:
            self.set_processvar(process_var)
        self.calc_dt()
        self.calc_error()
        p = self.calc_P()
        i = self.calc_I()
        d = self.calc_D()
        self.output = self.coerce(self.output + p + i + d, self.o_min, self.o_max)

