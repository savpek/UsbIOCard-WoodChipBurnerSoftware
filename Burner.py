# coding=utf-8
from time import sleep


class Burner():
    _screw_terminal = None
    _fan_terminal = None
    _fire_watch_terminal = None

    _ioCard = None

    def __init__(self, ioCard, ScrewTerminal, FanTerminal, FireWatchTerminal):
        self._ioCard = ioCard
        self._screw_terminal = ScrewTerminal
        self._fan_terminal = FanTerminal
        self._fire_watch_terminal = FireWatchTerminal

    def running(self):
        self._ioCard.set_terminal_high(self._fan_terminal)
        self._ioCard.set_terminal_high(self._screw_terminal)

    def disabled(self):
        self._ioCard.set_terminal_low(self._fan_terminal)
        self._ioCard.set_terminal_low(self._screw_terminal)

    def waiting(self):
        self._ioCard.set_terminal_high(self._fan_terminal)
        self._ioCard.set_terminal_low(self._screw_terminal)

    def get_fire_value(self):
        return self._ioCard.adc_of_terminal(self._fire_watch_terminal)

