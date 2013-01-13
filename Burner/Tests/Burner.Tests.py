# coding=utf-8
import unittest
import Burner.Burner
from mock import call, Mock
from Burner.IO.UsbCard import UsbCard

class BurnerTests(unittest.TestCase):
    _burner = None
    _iocard = None

    def setUp(self):
        self._iocard = Mock(spec=UsbCard)
        self._burner = Burner.Burner.Burner(self._iocard, "ScrewTerminal", "FanTerminal", "FireWatchTerminal")

    def test_wait_state_should_enable_fan_and_disable_screw(self):
        self._burner.waiting()
        self._iocard.set_terminal_high.assert_called_once_with("FanTerminal")
        self._iocard.set_terminal_low.assert_called_once_with("ScrewTerminal")

    def test_running_state_should_enable_fan_and_screw(self):
        self._burner.running()
        self._iocard.set_terminal_high.assert_has_calls([call("FanTerminal"), call("ScrewTerminal")])

    def test_disabled_state_should_disable_everything(self):
        self._burner.disabled()
        self._iocard.set_terminal_low.assert_has_calls([call("FanTerminal"), call("ScrewTerminal")])

    def test_fire_value_calls_correct_io_command_and_returns_results(self):
        self._iocard.adc_of_terminal.return_value = 10
        self.assertEqual(self._burner.get_fire_value(), 10)
        self._iocard.adc_of_terminal.assert_called_once_with("FireWatchTerminal")