class BurnerLogic():
    ScrewTime = 2 #How long screw runs.
    Delay = 20 #Delay in seconds.

    Enabled = False

    ScrewTerminalName = None
    FanTerminalName = None
    FireWatchTerminalName = None

    StatusMsg = ""

    FireWatchLimit = 10
    FireWatchLastValue = 0

    _ioCard = None
    _sleepMethod = None

    def __init__(self, ioCard, sleepMethod):
        self._ioCard = ioCard
        self._sleepMethod = sleepMethod

    def execute(self):
        if self.ScrewTime > self.Delay:
            self._disabled()
            raise ValueError, "Screw time should never be more than delay!"

        assert self.ScrewTerminalName is not None, "ScrewTerminalName"
        assert self.FanTerminalName is not None, "FanTerminalName"
        assert self.FireWatchTerminalName is not None, "FireWatchTerminalName"

        try:
            if self.Enabled:
                self._check_and_update_fire_watch()
                self._screw()
                self._wait()
            else:
                self._disabled()
        except:
            self._disabled()
            raise

    def _screw(self):
        self.StatusMsg = "Screw is running for {0} seconds.".format(self.ScrewTime)
        self._ioCard.set_terminal_high(self.FanTerminalName)
        self._ioCard.set_terminal_high(self.ScrewTerminalName)

        self._sleepMethod(self.ScrewTime)
        self._ioCard.set_terminal_low(self.ScrewTerminalName)

    def _wait(self):
        waitDuration = self.Delay - self.ScrewTime
        self.StatusMsg = "Waiting next cycle for {0} seconds.".format(waitDuration)

        self._sleepMethod(waitDuration)

    def _disabled(self):
        self._ioCard.set_terminal_low(self.FanTerminalName)
        self._ioCard.set_terminal_low(self.ScrewTerminalName)
        self._sleepMethod(0.5)
        self.StatusMsg = "Disabled."

    def _check_and_update_fire_watch(self):
        self.FireWatchLastValue = self._ioCard.adc_of_terminal(self.FireWatchTerminalName)

        if self.FireWatchLastValue < self.FireWatchLimit:
            raise ValueError(
                "Limit for fire brightness level broken! Expected value to be larger than {0}, but got {1}".format(
                    self.FireWatchLimit, self.FireWatchLastValue))

