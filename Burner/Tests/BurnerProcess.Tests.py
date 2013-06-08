# coding=utf-8
import unittest
from mock import Mock, call
from burner.burnercontroller import BurnerController
from burner.burnerprocess import BurnerProcess


class BurnerTests(unittest.TestCase):
    _burnerController = None
    _burner = None

    def setUp(self):
        self._burnerController = Mock(spec=BurnerController)
        self._burnerProcess = BurnerProcess(self._burnerController)

    def test_if_device_is_enabled_should_run_correct_routines(self):
        self._burnerProcess.ScrewSec = 1
        self._burnerProcess.DelaySec = 2
        self._burnerProcess.Enabled = True

        # On first tick screw and fan should go on.
        self._burnerController.tick.return_value = False
        self._burnerProcess._execute()
        self._burnerController.assert_has_calls([call.tick(), call.start_cycle(1, 2), call.light_sensor()])

        # Second tick. Screw stops now.
        self._burnerController.reset_mock()
        self._burnerController.tick.return_value = True  # Now screw is stopped.
        self._burnerProcess._execute()
        self._burnerController.assert_has_calls([call.tick()])

        # Third tick, everything keeps going.
        self._burnerController.reset_mock()
        self._burnerController.tick.return_value = True
        self._burnerProcess._execute()
        self._burnerController.assert_has_calls([call.tick()])

        # Fourth tick. Screw should start again because delay is over.
        self._burnerController.reset_mock()
        self._burnerController.tick.return_value = False  # Now screw is stopped.
        self._burnerProcess._execute()
        self._burnerController.assert_has_calls([call.tick(), call.start_cycle(1, 2), call.light_sensor()])

    def test_if_device_is_disabled_it_stops_after_routine(self):
        self._burnerProcess.Enabled = False

        self._burnerController.reset_mock()
        self._burnerController.tick.return_value = True
        self._burnerProcess._execute()
        self.assertEqual(self._burnerController.method_calls, [call.tick(), call.disable(), call.light_sensor()])

    def test_device_is_automatically_set_as_disabled_if_error_occurs(self):
        self._burnerProcess.Enabled = True
        self._burnerController.tick.side_effect = ValueError("Test error!")
        self._burnerProcess._execute()
        self.assertEqual(self._burnerProcess.Enabled, False)

    def test_if_runs_ok_set_status_as_status_is_running_and_ok(self):
        self._burnerProcess.ScrewSec = 1
        self._burnerProcess.DelaySec = 1
        self._burnerProcess.Enabled = True
        self._burnerProcess._execute()
        self.assertEqual(self._burnerProcess.Enabled, True)

    def test_if_fire_value_is_ok_keep_running(self):
        self._burnerProcess.Enabled = True
        self._burnerProcess.LightSensor = 100
        self._burnerController.light_sensor.return_value = 200
        self._burnerProcess._execute()
        self.assertEquals(self._burnerProcess.Enabled, True)

    def test_if_fire_value_is_not_ok_set_status_as_error_and_disable_device(self):
        self._burnerProcess.LightSensor = 100
        self._burnerController.light_sensor.return_value = 10
        self._burnerProcess._execute()
        self.assertEquals(self._burnerProcess.Enabled, False)
        self._burnerController.assert_has_calls(call.disable())

    def test_if_device_is_disabled_only_call_fire_value_and_disable(self):
        self._burnerProcess.Enabled = False
        self._burnerProcess._execute()
        self._burnerController.assert_has_calls(call.disable())

    def _event_result_collector(self, message):
        self.message = message

    def test_on_error_execute_error_event(self):
        self._burnerProcess.ErrorOccurredEvent = self._event_result_collector
        self._burnerController.tick.side_effect = ValueError("Error occurred!")
        self._burnerProcess._execute()
        self.assertEquals(self.message, "Error occurred!")