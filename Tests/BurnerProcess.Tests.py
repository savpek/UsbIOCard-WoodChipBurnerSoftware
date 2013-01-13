# coding=utf-8
import unittest
from mock import Mock, call
from BurnerController import BurnerController
from BurnerProcess import BurnerProcess

class BurnerTests(unittest.TestCase):
    _burnerController = None
    _burner = None

    def setUp(self):
        self._burnerController = Mock(spec=BurnerController)
        self._burnerProcess = BurnerProcess(self._burnerController)

    def test_firevalue_tick_will_be_called_once(self):
        self._burnerProcess._execute()
        self._burnerController.fire_value_tick.assert_called_once_with()

    def test_if_device_is_enabled_should_run_correct_routines(self):
        self._burnerProcess.ScrewSec = 1
        self._burnerProcess.DelaySec = 1
        self._burnerProcess.Enabled = True

        # On first tick screw and fan should go on.
        self._burnerController.screw_tick.return_value = False
        self._burnerController.delay_tick.return_value = False # Marks that invoke of start routine is required.
        self._burnerProcess._execute()
        self._burnerController.assert_has_calls([call.fire_value_tick(), call.screw_tick(), call.delay_tick(), call.screw_start(1), call.delay_start(2)])

        # Second tick. Screw stops now.
        self._burnerController.reset_mock()
        self._burnerController.screw_tick.return_value = False  # Now screw is stopped.
        self._burnerController.delay_tick.return_value = True
        self._burnerProcess._execute()
        self._burnerController.assert_has_calls([call.fire_value_tick(), call.screw_tick(), call.delay_tick()])

        # Third tick. Screw should start again because delay is over.
        self._burnerController.reset_mock()
        self._burnerController.screw_tick.return_value = False  # Now screw is stopped.
        self._burnerController.delay_tick.return_value = False  # Now delay is over.
        self._burnerProcess._execute()
        self._burnerController.assert_has_calls([call.fire_value_tick(), call.screw_tick(), call.delay_tick(), call.screw_start(1), call.delay_start(2)])

    def test_before_any_calls_process_status_is_not_initialized(self):
        self.assertEqual(self._burnerProcess.Status, "Not initialized.")

    def test_if_exception_is_raised_status_will_be_error_plus_message(self):
        exception = ValueError("Test error!")
        self._burnerController.screw_tick.side_effect = exception
        self._burnerProcess._execute()
        self.assertEqual(self._burnerProcess.Status, "Error: Test error!")

    def test_if_device_is_disabled_stop_after_routine(self):
        self._burnerProcess.Enabled = False

        self._burnerController.reset_mock()
        self._burnerController.screw_tick.return_value = False  # Now screw is stopped.
        self._burnerController.delay_tick.return_value = False  # Now delay is over.
        self._burnerProcess._execute()
        self.assertEqual(self._burnerController.method_calls, [call.fire_value_tick(), call.screw_tick(), call.delay_tick()])
