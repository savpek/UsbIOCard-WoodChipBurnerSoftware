import threading
from flask import Flask, render_template, request
import time
from BurnerLogic import BurnerLogic
from UsbCard import UsbCard

app = Flask(__name__)

def configure_burner():
    ioCard = UsbCard("COM3", 9600) # Define configurations for used IO card port.

    burner = BurnerLogic(ioCard, time.sleep)

    burner.Delay = 10       # Default setting on startup.
    burner.FanTime = 5      #
    burner.ScrewTime = 2    #

    burner.FanTerminalName = "2.T1"     # Look these from IO card printout.
    burner.ScrewTerminalName = "2.T2"   #

    return burner

class BurnerProcess(threading.Thread):
    exceptionMsg = ""

    def run(self):
        while True:
            try:
                burner.execute()
                self.exceptionMsg = ""
            except Exception as ex:
                self.exceptionMsg = ex

burner = configure_burner()

worker = BurnerProcess()
worker.start()

@app.route('/')
def index():
    burner.Delay = float(request.args.get('delay', burner.Delay))
    burner.ScrewTime = float(request.args.get('screwTime', burner.ScrewTime))
    burner.FanTime = float(request.args.get('fanTime', burner.FanTime))
    burner.Enabled = request.args.get('enabled', burner.Enabled) in ("True", True)

    return render_template('index.html',
        burner = burner,
        exceptionMessages = worker.exceptionMsg)

if __name__ == '__main__':
    app.run()
