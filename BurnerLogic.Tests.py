import unittest
from BurnerLogic import BurnerLogic
from mock import  call, MagicMock, Mock
from UsbCard import IoCardException, UsbCard

class UsbIoCardConnection_Tests(unittest.TestCase):
    def setUp(self):
        pass

    def test_execute_throws_exception_if_properties_are_not_set_correctly(self):
        burner = BurnerLogic(None, None)
        burner.Delay = 30
        burner.FanTime = 10     #This should throw error.
        burner.ScrewTime = 20   #because it is smaller than ScrewTime!
        self.assertRaises(ValueError, burner.Execute)

        burner.FanTime = 10     #This should throw error because it is > Delay
        burner.Delay = 5
        burner.ScrewTime = 2
        self.assertRaises(ValueError, burner.Execute)
        # If screwTime < FanTime, and FanTime < Delay. All possible combinations handled.

    def test_burner_should_set_delays_and_io_commands_correctly(self):
        externalCallsMock = MagicMock()
        timeMock = externalCallsMock
        ioCardMock = externalCallsMock

        burner = BurnerLogic(ioCardMock, timeMock)

        burner.Delay = 9
        burner.FanTime = 8
        burner.ScrewTime = 3
        burner.FanTerminalName = "FanTerminal"
        burner.ScrewTerminalName = "ScrewTerminal"

        burner.Execute()

        expectedCalls = [call.set_terminal_high("FanTerminal"),
                         call.set_terminal_high("ScrewTerminal"),
                         call.Sleep(3),
                         call.set_terminal_low("ScrewTerminal"),
                         call.Sleep(5),
                         call.set_terminal_low("FanTerminal"),
                         call.Sleep(1)]

        self.assertEqual(externalCallsMock.mock_calls, expectedCalls)

    def test_if_exception_occurs_all_outputs_should_be_set_off(self):
        ioCardMock = MagicMock()
        ioCardMock.set_terminal_high = Mock(side_effect=IoCardException("Boom"))
        timeMock = Mock()
        burner = BurnerLogic(ioCardMock, timeMock)

        burner.Delay = 9
        burner.FanTime = 8
        burner.ScrewTime = 3
        burner.FanTerminalName = "FanTerminal"
        burner.ScrewTerminalName = "ScrewTerminal"

        self.assertRaises(IoCardException, burner.Execute)

        ioCardMock.set_terminal_low.assert_any_call("FanTerminal")
        ioCardMock.set_terminal_low.assert_any_call("ScrewTerminal")
