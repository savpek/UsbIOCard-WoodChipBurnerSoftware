# coding=utf-8
import unittest
from mock import call, Mock
from Burner.Burner import Burner
from Burner.BurnerController import BurnerController

class BurnerControllerTests(unittest.TestCase):
    _burnerController = None
    _burner = None

    def setUp(self):
        self._burner = Mock(spec=Burner)
        self._burnerController = BurnerController(self._burner)

    def test_adc_value_calculates_average_from_list_correctly(self):
        self._burnerController._fireValue[0] = 60 # AVG should be 1 when list size is 60. (All rest are 0).
        self.assertEquals(1, self._burnerController.fire_value())

    def test_fire_value_tick_gets_burner_value_and_adds_it_to_history(self):
        self._burner.get_fire_value = Mock(return_value=40) # AVG should be 2, because 40+40+40 = 120.
        self._burnerController.fire_value_tick()  # Reads one value and adds it to history.
        self._burnerController.fire_value_tick()
        self._burnerController.fire_value_tick()
        self.assertEquals(self._burnerController.fire_value(), 2)

    def test_screw_start_and_screw_ticks_work_together_correctly(self):
        self._burnerController.screw_start(screw_ticks=2)
        self.assertEquals(self._burner.mock_calls, [call.running()])
        self._burnerController.screw_tick()
        self.assertEquals(self._burner.mock_calls, [call.running()])
        self._burnerController.screw_tick() # 2 seconds (2 ticks) done.
        self.assertEquals(self._burner.mock_calls, [call.running(), call.waiting()])

    def test_delay_tick_works_correctly(self):
        self._burnerController.delay_start(delay_ticks=2)
        self.assertEquals(self._burnerController.delay_tick(), False)
        self.assertEquals(self._burnerController.delay_tick(), True) # This can be used to trigger new cycle etc...

    def test_disable_calls_burner_disable(self):
        self._burnerController.disable()
        self._burner.disabled.assert_called_once_with()