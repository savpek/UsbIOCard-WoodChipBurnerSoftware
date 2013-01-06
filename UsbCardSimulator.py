class IoCardException(Exception):
    pass


class UsbCard:
    ERROR_KEYWORD = "ERROR:"
    TIMEOUT = 0.10  # How long input is waited after command.
    # This delay is kept after every command call.
    READ_MAX_COUNT = 200

    CommandsReceived = None

    def __init__(self, port, speed, serialInterface=None):
        pass

    def read_terminal(self, terminal_name):
        return "HIGH"

    def set_terminal_high(self, terminal_name):
        pass

    def set_terminal_low(self, terminal_name):
        pass

    def adc_of_terminal(self, terminal_name):
        return 50