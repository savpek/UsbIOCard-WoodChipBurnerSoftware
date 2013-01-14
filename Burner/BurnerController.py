# coding=utf-8

class BurnerController:
    VALUE_BUFFER_SIZE = 60
    APROX_TICK_TIME_SEC = 1

    _screw_ticks = 0
    _delay_ticks = 0

    _fireValue = None
    _valueTicks = 0
    _burner = None

    def __init__(self, burner):
        self._burner = burner
        self._fireValue = [0] * self.VALUE_BUFFER_SIZE

    def fire_value_tick(self):
        self._valueTicks += 1
        self._fireValue[self._valueTicks % self.VALUE_BUFFER_SIZE] = self._burner.get_fire_value()

    def screw_start(self, screw_ticks):
        self._burner.running()
        self._screw_ticks = screw_ticks

    def screw_tick(self):
        self._screw_ticks -= 1
        if self._screw_ticks <= 0:
            self._burner.waiting()

    def delay_start(self, delay_ticks):
        self._delay_ticks = delay_ticks

    def delay_tick(self):
        self._delay_ticks -= 1
        if self._delay_ticks <= 0:
            return True
        return False

    def fire_value(self):
        if sum(self._fireValue) is 0:
            return 0
        return sum(self._fireValue)/self.VALUE_BUFFER_SIZE

    def disable(self):
        self._burner.disabled()