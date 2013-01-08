# coding=utf-8
import threading

class BurnerProcess(threading.Thread):
    _controller = None


    def __init__(self, burner):
        super(BurnerProcess, self).__init__()
        self._controller = burner
        pass

    def run(self):
        pass

    def _excecute(self):
        pass