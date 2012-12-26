import time

class BurnerLogic():
    ScrewTime = 2 #How long screw runs.
    FanTime = 9 #How long fan will be on.
    Delay = 20 #Delay in seconds.

    ScrewTerminalName = None
    FanTerminalName = None

    _ioCard = None
    _time = None

    def __init__(self, ioCard, time):
        self._ioCard = ioCard
        self._time = time

    def Execute(self):
        if self.ScrewTime > self.FanTime:
            raise ValueError, "ScrewTime should never be more than FanTime!"
        if self.FanTime > self.Delay:
            raise ValueError, "FanTime should never be more than Delay!"

        try:
            self._ioCard.set_terminal_high(self.FanTerminalName)
            self._ioCard.set_terminal_high(self.ScrewTerminalName)

            self._time.Sleep(self.ScrewTime)
            self._ioCard.set_terminal_low(self.ScrewTerminalName)

            self._time.Sleep(self.FanTime - self.ScrewTime)
            self._ioCard.set_terminal_low(self.FanTerminalName)

            self._time.Sleep(self.Delay - self.FanTime)
        except:
            self._ioCard.set_terminal_low(self.FanTerminalName)
            self._ioCard.set_terminal_low(self.ScrewTerminalName)
            raise



