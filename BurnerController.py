# coding=utf-8
import threading

class BurnerController:
    VALUE_BUFFER_SIZE = 60
    APROX_TICK_TIME_SEC = 1

    ScrewTicks = 0
    DelayTicks = 0

    Enabled = False

    _fireValue = None
    _valueTicks = 0
    _burner = None

    def __init__(self, burner):
        self._burner = burner
        self._fireValue = [0] * self.VALUE_BUFFER_SIZE

    def _firevalue_tick(self):
        self._valueTicks += 1
        self._fireValue[self._valueTicks % self.VALUE_BUFFER_SIZE] = self._burner.firewatch_value()

    def _screw_start(self, screw_ticks):
        self._burner._screw()
        self.ScrewTicks = screw_ticks

    def _screw_tick(self):
        self.ScrewTicks -= 1
        if self.ScrewTicks <= 0:
            self._burner._stopped()

    def _delay_start(self, delay_ticks):
        self.DelayTicks = delay_ticks

    def _delay_tick(self):
        self.DelayTicks -= 1
        if self.DelayTicks <= 0:
            return True
        return False

    def fire_value(self):
        if sum(self._fireValue) is 0:
            return 0
        return sum(self._fireValue)/self.VALUE_BUFFER_SIZE