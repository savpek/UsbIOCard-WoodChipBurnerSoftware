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

    def test_tick_gets_burner_value_and_adds_it_to_history(self):
        self._burner.get_fire_value = Mock(return_value=40) # AVG should be 2, because 40+40+40 = 120.
        self._burnerController.tick()  # Reads one value and adds it to history.
        self._burnerController.tick()
        self._burnerController.tick()
        self.assertEquals(self._burnerController.fire_value(), 2)

    def test_tick_works_correctly(self):
        self._burnerController.start_cycle(screw_ticks=1, delay_ticks=1)
        self.assertEquals(self._burner.mock_calls, [call.running()])
        self.assertEqual(self._burnerController.tick(), True) # Device is running.
        self.assertEquals(self._burner.mock_calls, [call.running(), call.get_fire_value(),  call.waiting()])
        self.assertEqual(self._burnerController.tick(), False) # Device is not running anymore.
        self.assertEquals(self._burner.mock_calls,
            [call.running(),
             call.get_fire_value(),
             call.waiting(),
             call.get_fire_value(),
             call.disabled()])

    def test_disable_calls_burner_disable(self):
        self._burnerController.disable()
        self._burner.disabled.assert_called_once_with()