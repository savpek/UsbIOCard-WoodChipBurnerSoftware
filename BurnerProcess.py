# coding=utf-8
import threading

class BurnerProcess(threading.Thread):
    VALUE_BUFFER_SIZE = 60
    APROX_TICK_TIME_SEC = 1

    ScrewTicks = 0
    Enabled = False

    _fireValue = [0] * VALUE_BUFFER_SIZE
    _ticks = 0
    _burner = None


    def __init__(self, burner):
        super(BurnerProcess, self).__init__()
        self._burner = burner
        pass

    def run(self):
        pass

    def _excecute(self):
        pass

    def _cycle_start(self, screw_ticks):
        self._burner._screw()
        self.ScrewTicks = screw_ticks

    def _cycle_tick(self):
        self._fireValue[self._ticks % self.VALUE_BUFFER_SIZE] = self._burner.firewatch_value()
        self._ticks += 1
        self.ScrewTicks -= 1
        if self.ScrewTicks <= 0:
            self._burner._stopped()


    def fire_value(self):
        if sum(self._fireValue) is 0:
            return 0
        return sum(self._fireValue)/60