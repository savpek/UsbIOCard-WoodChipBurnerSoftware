__author__ = 'savpek'

from burner.burner import Burner
from burner.burnercontroller import BurnerController
from burner.burnerprocess import BurnerProcess
from burner.io.usbcard_simulator import UsbCardSimulator


def get_burner_process():
    ioCard = UsbCardSimulator("/dev/ttyUSB0", 9600)  # Define configurations for used IO card port.
    burner = Burner(ioCard, ScrewTerminal="2.T2", FanTerminal="2.T1", FireWatchTerminal="7.T0.ADC0")
    burnerController = BurnerController(burner)
    burnerProcess = BurnerProcess(burnerController)

    # Initial values ...
    burnerProcess.ScrewSec = 1
    burnerProcess.DelaySec = 4
    return burnerProcess