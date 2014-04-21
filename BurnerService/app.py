import json
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

def get_burner_process(iodriver):
    burner = Burner(iodriver, ScrewTerminal="2.T2", FanTerminal="2.T1", FireWatchTerminal="7.T0.ADC0")
    controller = BurnerController(burner)
    process = BurnerProcess(controller)

    # Initial values
    process.ScrewSec = 1
    process.DelaySec = 4
    return process


burnerProcess = get_burner_process(iocard)
burnerProcess.start()

urls = (
    '/status/', 'CurrentBurnerStatus',
    '/update/', 'CurrentBurnerStatus'
)


class CurrentBurnerStatus:
    def __init__(self):
        pass

    def GET(self):
        return {"ScrewSec": burnerProcess.ScrewSec,
                "DelaySec": burnerProcess.DelaySec,
                "Enabled": burnerProcess.Enabled,
                "LightSensor": BurnerProcess.LightSensor}

    def PUT(self):
        data = json.loads(web.data())
        burnerProcess.ScrewSec = data["ScrewSec"]
        burnerProcess.DelaySec = data["DelaySec"]
        burnerProcess.Enabled = data["Enabled"]
        return web.ok()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()