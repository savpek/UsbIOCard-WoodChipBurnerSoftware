from threading import Thread
import threading
from flask import Flask, render_template, request
import time
from BurnerLogic import BurnerLogic
from UsbCard import UsbCard

app = Flask(__name__)

ioCard = UsbCard("COM3", 9600)
burner = BurnerLogic(ioCard, time.sleep)

burner.Delay = 10
burner.FanTime = 5
burner.ScrewTime = 2

burner.FanTerminalName = "2.T1"
burner.ScrewTerminalName = "2.T2"

class Runner(threading.Thread):
    exceptionMsg = ""

    def run(self):
        while True:
            try:
                burner.execute()
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
    burner.Enabled = request.args.get('enabled', burner.Enabled) in ("True", True)

    return render_template('index.html',
        delay = burner.Delay,
        fanTime = burner.FanTime,
        screwTime = burner.ScrewTime,
        status = burner.StatusMsg,
        exceptionMessages = worker.exceptionMsg,
        enabled = burner.Enabled)

if __name__ == '__main__':
    #app.debug = True
    app.run()
