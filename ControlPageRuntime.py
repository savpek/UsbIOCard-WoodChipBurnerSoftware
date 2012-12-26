from threading import Thread
import threading
from flask import Flask, render_template, request
import time
from BurnerLogic import BurnerLogic
from UsbCard import UsbCard

app = Flask(__name__)

ioCard = UsbCard("COM3", 9600)
burner = BurnerLogic(ioCard, time.sleep)

burner.Delay = 3
burner.FanTime = 1
burner.ScrewTime = 1

burner.FanTerminalName = "2.T0"
burner.ScrewTerminalName = "2.T1"

class Runner(threading.Thread):
    exceptionMsg = ""
    Enabled = False

    def run(self):
        while True:
            time.sleep(0.5)
            try:
                if self.Enabled:
                    burner.Execute()
                    self.exceptionMsg = ""
            except Exception as ex:
                self.exceptionMsg = ex

worker = Runner()
worker.start()

@app.route('/')
def hello_world():
    burner.Delay = float(request.args.get('delay', burner.Delay))
    burner.ScrewTime = float(request.args.get('screwTime', burner.ScrewTime))
    burner.FanTime = float(request.args.get('fanTime', burner.FanTime))
    worker.Enabled = request.args.get('enabled', worker.Enabled) in ("True", True)

    return render_template('index.html',
        delay = burner.Delay,
        fanTime = burner.FanTime,
        screwTime = burner.ScrewTime,
        status = "Status",
        exceptionMessages = worker.exceptionMsg,
        enabled = worker.Enabled)

if __name__ == '__main__':
    #app.debug = True
    app.run()
