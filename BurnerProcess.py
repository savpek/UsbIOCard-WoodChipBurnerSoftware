# coding=utf-8
import threading
import time

class BurnerProcess(threading.Thread):
    _controller = None

    ScrewSec = 0
    DelaySec = 0
    Enabled = False
    FireLimit = 0

    Status = "Not initialized."

    def __init__(self, burner):
        super(BurnerProcess, self).__init__()
        self._controller = burner
        pass

    def run(self):
        while True:
            time.sleep(0.9) # This makes time more nearly second since some time is wasted on io card operations.
            self._execute()

    def _execute(self):
        try:
            self._controller.fire_value_tick()
            self._controller.screw_tick()

            if self._controller.delay_tick() is False and self.Enabled is True:
                self._controller.screw_start(self.ScrewSec)
                self._controller.delay_start(self.DelaySec+self.ScrewSec)

            if self._controller.fire_value() < self.FireLimit:
                raise ValueError("Fire value limit is over feedback!")

            if self.Enabled is False:
                self._controller.disable()

            self.Status = "Device status is OK!"
        except Exception, e:
            self.Status = "Error: " + e.message
            self.Enabled = False

    def get_fire_value(self):
        return self._controller.fire_value()