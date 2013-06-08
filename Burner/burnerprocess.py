# coding=utf-8
import threading
import time


class BurnerProcess(threading.Thread):
    _controller = None

    ScrewSec = 0
    DelaySec = 0
    Enabled = False
    LightSensor = 0

    def _do_nothing(self, message):
        pass

    ErrorOccurredEvent = _do_nothing

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
            if self._controller.tick() is False and self.Enabled is True:
                self._controller.start_cycle(self.ScrewSec, self.DelaySec)

            if self.Enabled is False:
                self._controller.disable()

            if self._controller.light_sensor() < self.LightSensor:
                raise ValueError("Fire value limit is over feedback!")
        except Exception, e:
            self.Enabled = False
            self.ErrorOccurredEvent(e.message)

    def get_fire_value(self):
        return self._controller.light_sensor()