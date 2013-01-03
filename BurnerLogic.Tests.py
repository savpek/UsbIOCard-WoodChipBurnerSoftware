import unittest
from BurnerLogic import BurnerLogic
from mock import  call, MagicMock, Mock
from UsbCard import IoCardException, UsbCard

class UsbIoCardConnection_Tests(unittest.TestCase):
    _burner = None
    _externalCallsMock = None

    def setUp(self):
        self._externalCallsMock = MagicMock()
        self._burner = BurnerLogic(self._externalCallsMock, self._externalCallsMock)

        self._burner.Delay = 9
        self._burner.ScrewTime = 3
        self._burner.FanTerminalName = "FanTerminal"
        self._burner.ScrewTerminalName = "ScrewTerminal"
        self._burner.FireWatchTerminalName = "FireWatchTerminal"

    def test_execute_throws_exception_if_properties_are_not_set_correctly_and_disables_outputs(self):
        burner = BurnerLogic(None, None)
        burner._disabled = Mock()
        burner.Delay = 10       # This throws exception!
        burner.ScrewTime = 20   # because it is smaller than ScrewTime!
        self.assertRaises(ValueError, burner.execute)
        burner._disabled.assert_called_once_with()

    def test_if_exception_occurs_all_outputs_should_be_set_off(self):
        ioCardMock = MagicMock()
        ioCardMock.adc_of_terminal = Mock(side_effect=IoCardException("Boom"))
        timeMock = Mock()
        self._burner = BurnerLogic(ioCardMock, timeMock)
        self._burner.FanTerminalName = "FanTerminal"
        self._burner.ScrewTerminalName = "ScrewTerminal"
        self._burner.FireWatchTerminalName = "FireWatchTerminal"
        self._burner.Enabled = True

        self.assertRaises(IoCardException, self._burner.execute)

        ioCardMock.set_terminal_low.assert_any_call("FanTerminal")
        ioCardMock.set_terminal_low.assert_any_call("ScrewTerminal")

    def test_screw_state(self):
        self._burner._screw()

        expectedCalls = [call.set_terminal_high("FanTerminal"),
                         call.set_terminal_high("ScrewTerminal"),
                         call.Sleep(3),
                         call.set_terminal_low("ScrewTerminal")]

        self.assertEqual("Screw is running for 3 seconds.", self._burner.StatusMsg)
        self.assertEqual(self._externalCallsMock.mock_calls, expectedCalls)

    def test_wait_state(self):
        self._burner._wait()

        expectedCalls = [call.Sleep(6)]

        self.assertEqual("Waiting next cycle for 6 seconds.", self._burner.StatusMsg)
        self.assertEqual(self._externalCallsMock.mock_calls, expectedCalls)

    def test_disabled_state(self):
        self._burner._disabled()

        expectedCalls = [call.set_terminal_low("FanTerminal"),
                         call.set_terminal_low("ScrewTerminal"),
                         call.Sleep(0.5)]

        self.assertEqual("Disabled.", self._burner.StatusMsg)
        self.assertEqual(self._externalCallsMock.mock_calls, expectedCalls)

    def test_fire_watch_update_last_value_correctly(self):
        self._externalCallsMock.adc_of_terminal = Mock(return_value=100)
        self._burner.FireWatchLimit = 10 # This is less than 100, so everything is ok.

        self._burner._check_and_update_fire_watch()
        self.assertEqual(100, self._burner.FireWatchLastValue)
        self._externalCallsMock.adc_of_terminal.assert_called_once_with("FireWatchTerminal")

    def test_fire_watch_throw_exception_if_read_value_is_below_defined_limit(self):
        self._externalCallsMock.adc_of_terminal = Mock(return_value=100)
        self._burner.FireWatchLimit = 150 # This is more than 100, so everything is NOT ok.

        self.assertRaises(ValueError, self._burner._check_and_update_fire_watch)