# coding=utf-8
import unittest
from Burner import Burner
from mock import call, MagicMock, Mock
from BurnerProcess import BurnerProcess
from UsbCard import IoCardException


class BurnerTests(unittest.TestCase):
    _burnerProcess = None
    _burner = None

    def setUp(self):
        self._burner = Mock(spec=Burner)
        self._burnerProcess = BurnerProcess(self._burner)

    def test_adc_value_calculates_average_from_list_correctly(self):
        self._burnerProcess._fireValue[0] = 60 # AVG should be 1 when list size is 60. (All rest are 0).
        self.assertEquals(1, self._burnerProcess.fire_value())

    def test_cycle_tick_gets_fireburner_value_and_adds_it_to_history(self):
        self._burner.firewatch_value = Mock(return_value=40) # AVG should be 2, because 40+40+40 = 120.
        self._burnerProcess._cycle_tick(1)  # Reads one value and adds it to history.
        self._burnerProcess._cycle_tick(1)
        self._burnerProcess._cycle_tick(1)
        self.assertEquals(self._burnerProcess.fire_value(), 2)

    def test_cycle_start_and_cycles_work_together_correctly(self):
        self._burnerProcess.Enabled = True
        self._burnerProcess._cycle_start(screw_ticks=2)
        self.assertEquals(self._burner.mock_calls, [call._screw()])
        self._burnerProcess._cycle_tick()
        self.assertEquals(self._burner.mock_calls, [call._screw(), call.firewatch_value()])
        self._burnerProcess._cycle_tick() # 2 seconds (2 ticks) done.
        self.assertEquals(self._burner.mock_calls, [call._screw(),
                                                    call.firewatch_value(),
                                                    call.firewatch_value(),
                                                    call._stopped()])

    # In some tests we don't want check certain calls.
    def compare_calls_without_firewatch(self, value, list):
        return filter(lambda x: x != value, list)