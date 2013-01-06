# coding=utf-8
import threading


class BurnerProcess(threading.Thread):
    Delay = None
    ScrewTime = None
    _fireValue = [0]*60

    def __init__(self, burner):
        super(BurnerProcess, self).__init__()
        pass

    def run(self):
        pass

    def _excecute(self):
        pass

    def _cycle_start(self, screw_time, delay):
        pass

    def _cycle_tick(self, tick_time_s):
        pass