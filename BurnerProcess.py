# coding=utf-8
import threading

class BurnerProcess(threading.Thread):
    _controller = None

    ScrewSec = 0
    DelaySec = 0
    Enabled = False

    Status = "Not initialized."

    def __init__(self, burner):
        super(BurnerProcess, self).__init__()
        self._controller = burner
        pass

    def run(self):
        pass

    def _execute(self):
        try:
            self._controller.fire_value_tick()
            self._controller.screw_tick()
            if self._controller.delay_tick() is False and self.Enabled is True:
                self._controller.screw_start(self.ScrewSec)
                self._controller.delay_start(self.DelaySec+self.ScrewSec)
        except Exception, e:
            self.Status = "Error: " + e.message

    def get_fire_value(self):
        return self._controller.fire_value()

    def disable(self):
        pass