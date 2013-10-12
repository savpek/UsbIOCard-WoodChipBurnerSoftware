import datetime


class IoCardException(Exception):
    pass


class UsbCardSimulator:
    Log = None
    AdcValue = 50

    FanState = "OFF"
    ScrewState = "OFF"

    def _do_nothing(self, message):
        pass

    CardActionInvoked = _do_nothing

    def __init__(self, port, speed, serialInterface=None):
        self.Log = ""

    def read_terminal(self, terminal_name):
        self._send_action_information("read_terminal", terminal_name)
        return "HIGH"

    def set_terminal_high(self, terminal_name):
        self._send_action_information("set_terminal_high", terminal_name)
        if terminal_name == "2.T1":
            self.FanState = "ON"
        if terminal_name == "2.T2":
            self.ScrewState = "ON"


    def set_terminal_low(self, terminal_name):
        if terminal_name == "2.T1":
            self.FanState = "OFF"
        if terminal_name == "2.T2":
            self.ScrewState = "OFF"
        self._send_action_information("set_terminal_low", terminal_name)

    def adc_of_terminal(self, terminal_name):
        self._send_action_information("acd_of_terminal", terminal_name)
        return self.AdcValue

    def _send_action_information(self, action, terminal_name):
        message = "{0} Called: {1} with terminal name: {2}\n".format(
            datetime.datetime.now().strftime("%d/%m/%y %H:%S"),
            action,
            terminal_name)
        self.CardActionInvoked(message)