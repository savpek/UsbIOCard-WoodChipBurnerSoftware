# coding=utf-8
import unittest
from mock import Mock, call
from Burner.BurnerController import BurnerController
from Burner.BurnerProcess import BurnerProcess

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
        self._burnerController.assert_has_calls([call.tick(), call.start_cycle(1, 2), call.fire_value()])

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
        self._burnerController.assert_has_calls([call.tick(), call.start_cycle(1, 2), call.fire_value()])

    def test_before_any_calls_process_status_is_not_initialized(self):
        self.assertEqual(self._burnerProcess.Status, "Not initialized.")

    def test_if_exception_is_raised_status_will_be_error_plus_message(self):
        self._burnerController.tick.side_effect = ValueError("Test error!")
        self._burnerProcess._execute()
        self.assertEqual(self._burnerProcess.Status, "Error: Test error!")

    def test_if_device_is_disabled_it_stops_after_routine(self):
        self._burnerProcess.Enabled = False

        self._burnerController.reset_mock()
        self._burnerController.tick.return_value = True
        self._burnerProcess._execute()
        self.assertEqual(self._burnerController.method_calls, [call.tick(), call.disable(), call.fire_value()])

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
        self.assertEquals(self._burnerProcess.Status, "Device status is OK!")

    def test_if_fire_value_is_ok_keep_running(self):
        self._burnerProcess.Enabled = True
        self._burnerProcess.FireLimit = 100
        self._burnerController.fire_value.return_value = 200
        self._burnerProcess._execute()
        self.assertEquals(self._burnerProcess.Enabled, True)
        self.assertNotEquals(self._burnerProcess.Status, "Error: Fire value limit is over feedback!")

    def test_if_fire_value_is_not_ok_set_status_as_error_and_disable_device(self):
        self._burnerProcess.FireLimit = 100
        self._burnerController.fire_value.return_value = 10
        self._burnerProcess._execute()
        self.assertEquals(self._burnerProcess.Enabled, False)
        self.assertEquals(self._burnerProcess.Status, "Error: Fire value limit is over feedback!")
        self._burnerController.assert_has_calls(call.disable())

    def test_if_device_is_disabled_only_call_fire_value_and_disable(self):
        self._burnerProcess.Enabled = False
        self._burnerProcess._execute()
        self._burnerController.assert_has_calls(call.disable())

