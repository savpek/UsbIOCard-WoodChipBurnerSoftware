# coding=utf-8
import unittest
from mock import call, Mock
from Burner import Burner
from BurnerController import BurnerController

class BurnerControllerTests(unittest.TestCase):
    _burnerController = None
    _burner = None

    def setUp(self):
        self._burner = Mock(spec=Burner)
        self._burnerController = BurnerController(self._burner)

    def test_adc_value_calculates_average_from_list_correctly(self):
        self._burnerController._fireValue[0] = 60 # AVG should be 1 when list size is 60. (All rest are 0).
        self.assertEquals(1, self._burnerController.fire_value())

    def test_firevalue_tick_gets_fireburner_value_and_adds_it_to_history(self):
        self._burner.firewatch_value = Mock(return_value=40) # AVG should be 2, because 40+40+40 = 120.
        self._burnerController._firevalue_tick()  # Reads one value and adds it to history.
        self._burnerController._firevalue_tick()
        self._burnerController._firevalue_tick()
        self.assertEquals(self._burnerController.fire_value(), 2)

    def test_screw_start_and_screw_ticks_work_together_correctly(self):
        self._burnerController._screw_start(screw_ticks=2)
        self.assertEquals(self._burner.mock_calls, [call._screw()])
        self._burnerController._screw_tick()
        self.assertEquals(self._burner.mock_calls, [call._screw()])
        self._burnerController._screw_tick() # 2 seconds (2 ticks) done.
        self.assertEquals(self._burner.mock_calls, [call._screw(), call._stopped()])

    def test_delay_tick_works_correctly(self):
        self._burnerController._delay_start(delay_ticks=2)
        self.assertEquals(self._burnerController._delay_tick(), False)
        self.assertEquals(self._burnerController._delay_tick(), True) # This can be used to trigger new cycle etc...
