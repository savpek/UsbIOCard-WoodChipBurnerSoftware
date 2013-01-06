import datetime


class IoCardException(Exception):
    pass


class UsbCard:
    Log = None

    def __init__(self, port, speed, serialInterface=None):
        self.Log = ""

    def read_terminal(self, terminal_name):
        self._write_action_log("read_terminal", terminal_name)
        return "HIGH"

    def set_terminal_high(self, terminal_name):
        self._write_action_log("set_terminal_high", terminal_name)

    def set_terminal_low(self, terminal_name):
        self._write_action_log("set_terminal_low", terminal_name)

    def adc_of_terminal(self, terminal_name):
        self._write_action_log("acd_of_terminal", terminal_name)
        return 50

    def _write_action_log(self, action, terminal_name):
        self.Log += "{0} Called: {1} with terminal name: {2}\n".format(
            datetime.datetime.now().strftime("%d/%m/%y %H:%S"),
            action,
            terminal_name)