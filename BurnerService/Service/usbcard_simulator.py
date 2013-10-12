import datetime


class IoCardException(Exception):
    pass


class UsbCardSimulator:
    AdcValueFake = 50

    _message_writer = None

    def _do_nothing(self, message):
        pass

    CardActionInvoked = _do_nothing

    def __init__(self, message_writer):
        self._message_writer = message_writer

    def read_terminal(self, terminal_name):
        self._send_action_information("read_terminal", terminal_name)
        return "HIGH"

    def set_terminal_high(self, terminal_name):
        self._send_action_information("set_terminal_high", terminal_name)


    def set_terminal_low(self, terminal_name):
        self._send_action_information("set_terminal_low", terminal_name)

    def adc_of_terminal(self, terminal_name):
        self._send_action_information("acd_of_terminal", terminal_name)
        return self.AdcValueFake

    def _send_action_information(self, action, terminal_name):
        message = "{0} Called: {1} with terminal name: {2}\n".format(
            datetime.datetime.now().strftime("%d/%m/%y %H:%S"),
            action,
            terminal_name)
        self._message_writer(message)