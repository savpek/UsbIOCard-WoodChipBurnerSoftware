import web
import logging

from Service.burnerprocess import BurnerProcess
from Service.burnercontroller import BurnerController
from Service.burner import Burner
from Service.usbcard_simulator import UsbCardSimulator

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def writer(message):
    logging.debug(message)


iocard = UsbCardSimulator(writer)


def get_burner_process(iocard):
    burner = Burner(iocard, ScrewTerminal="2.T2", FanTerminal="2.T1", FireWatchTerminal="7.T0.ADC0")
    controller = BurnerController(burner)
    process = BurnerProcess(controller)

    # Initial values ...
    process.ScrewSec = 1
    process.DelaySec = 4
    return process


burnerProcess = get_burner_process(iocard)
burnerProcess.start()

urls = (
    '/', 'ListUsers'
)


class CurrentBurnerStatus:
    def __init__(self):
        pass

    def GET(self):
        return "Foo"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()