# coding=utf-8
from time import sleep


class Burner():
    ScrewTerminalName = None
    FanTerminalName = None
    FireWatchTerminalName = None

    _ioCard = None

    def __init__(self, ioCard):
        self._ioCard = ioCard

    def running(self):
        self._ioCard.set_terminal_high(self.FanTerminalName)
        self._ioCard.set_terminal_high(self.ScrewTerminalName)

    def disabled(self):
        self._ioCard.set_terminal_low(self.FanTerminalName)
        self._ioCard.set_terminal_low(self.ScrewTerminalName)

    def waiting(self):
        self._ioCard.set_terminal_high(self.FanTerminalName)
        self._ioCard.set_terminal_low(self.ScrewTerminalName)

    def get_fire_value(self):
        return self._ioCard.adc_of_terminal(self.FireWatchTerminalName)

