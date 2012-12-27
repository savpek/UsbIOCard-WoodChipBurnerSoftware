import time

class BurnerLogic():
    ScrewTime = 2 #How long screw runs.
    FanTime = 9 #How long fan will be on.
    Delay = 20 #Delay in seconds.

    Enabled = False

    ScrewTerminalName = None
    FanTerminalName = None

    StatusMsg = ""

    _ioCard = None
    _sleepFunc = None

    def __init__(self, ioCard, time):
        self._ioCard = ioCard
        self._sleepFunc = time

    def execute(self):
        if self.ScrewTime > self.FanTime:
            self._disabled()
            raise ValueError, "ScrewTime should never be more than FanTime!"
        if self.FanTime > self.Delay:
            self._disabled()
            raise ValueError, "FanTime should never be more than Delay!"

        try:
            if self.Enabled:
                self._screw()
                self._fan()
                self._wait()
            else:
                self._disabled()
        except:
            self._disabled()
            raise

    def _screw(self):
        self.StatusMsg = "Screw and fan are running for {0} seconds.".format(self.ScrewTime)
        self._ioCard.set_terminal_high(self.FanTerminalName)
        self._ioCard.set_terminal_high(self.ScrewTerminalName)

        self._sleepFunc(self.ScrewTime)
        self._ioCard.set_terminal_low(self.ScrewTerminalName)

    def _fan(self):
        fanDuration = self.FanTime - self.ScrewTime
        self.StatusMsg = "Fan is running for {0} seconds.".format(fanDuration)

        self._sleepFunc(fanDuration)
        self._ioCard.set_terminal_low(self.FanTerminalName)

    def _wait(self):
        waitDuration = self.Delay - self.FanTime
        self.StatusMsg = "Waiting next cycle for {0} seconds.".format(waitDuration)

        self._sleepFunc(waitDuration)

    def _disabled(self):
        self._ioCard.set_terminal_low(self.FanTerminalName)
        self._ioCard.set_terminal_low(self.ScrewTerminalName)
        self._sleepFunc(0.5)
        self.StatusMsg = "Disabled."


