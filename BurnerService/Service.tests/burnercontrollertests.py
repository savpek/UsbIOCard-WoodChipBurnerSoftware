# coding=utf-8
import unittest
import mock
from Service.burnercontroller import BurnerController


class BurnerControllerTests(unittest.TestCase):
    _burnerController = None
    _burner = None

    def setUp(self):
        self._burner = mock.Mock()
        self._burner.disabled = mock.Mock()
        self._burner.running = mock.Mock()
        self._burner.get_fire_value = mock.Mock()
        self._burner.waiting = mock.Mock()
        self._burnerController = BurnerController(self._burner)

    def test_adc_value_calculates_average_from_list_correctly(self):
        self._burnerController._fireValue[0] = 60 # AVG should be 1 when list size is 60. (All rest are 0).
        self.assertEquals(1, self._burnerController.light_sensor())

    def test_tick_gets_burner_value_and_adds_it_to_history(self):
        self._burner.get_fire_value = mock.Mock(return_value=40) # AVG should be 2, because 40+40+40 = 120.
        self._burnerController.tick()  # Reads one value and adds it to history.
        self._burnerController.tick()
        self._burnerController.tick()
        self.assertEquals(self._burnerController.light_sensor(), 2)

    def test_tick_works_correctly(self):
        self._burnerController.start_cycle(screw_ticks=1, delay_ticks=1)
        self.assertEquals(self._burner.mock_calls, [mock.call.running()])
        self.assertEqual(self._burnerController.tick(), True) # Device is running.
        self.assertEquals(self._burner.mock_calls, [mock.call.running(), mock.call.get_fire_value(),  mock.call.waiting()])
        self.assertEqual(self._burnerController.tick(), False) # Device is not running anymore.
        self.assertEquals(self._burner.mock_calls,
            [mock.call.running(),
             mock.call.get_fire_value(),
             mock.call.waiting(),
             mock.call.get_fire_value(),
             mock.call.disabled()])

    def test_disable_calls_burner_disable(self):
        self._burnerController.disable()
        self._burner.disabled.assert_called_once()