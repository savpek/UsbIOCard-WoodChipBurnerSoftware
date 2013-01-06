import threading
from flask import Flask, render_template, request
import time
import flask
from BurnerLogic import BurnerLogic
#from UsbCard import UsbCard
from UsbCardSimulator import UsbCard

app = Flask(__name__)

def configure_burner():
    ioCard = UsbCard("/dev/ttyUSB0", 9600) # Define configurations for used IO card port.

    burner = BurnerLogic(ioCard, time.sleep)

    burner.Delay = 10       # Default setting on startup.
    burner.ScrewTime = 2    #

    burner.FanTerminalName = "2.T1"     # Look these from IO card printout.
    burner.ScrewTerminalName = "2.T2"   #
    burner.FireWatchTerminalName = "7.T0.ADC0"   #

    return burner


class BurnerProcess(threading.Thread):
    exceptionMsg = ""

    def run(self):
        while True:
            try:
                burner.execute()
                self.exceptionMsg = ""
            except Exception as ex:
                self.exceptionMsg = ex.message

burner = configure_burner()

worker = BurnerProcess()
worker.start()

#@app.route('/')
def index():
    burner.Delay = float(request.args.get('delay', burner.Delay))
    burner.ScrewTime = float(request.args.get('screwTime', burner.ScrewTime))
    burner.Enabled = request.args.get('enabled', burner.Enabled) in ("True", True)
    burner.FireWatchLimit = float(request.args.get('fireWatchLimit', burner.FireWatchLimit))

    return render_template('index.html',
        burner=burner,
        exceptionMessages=worker.exceptionMsg)


@app.route('/')
def index():
    return render_template('settings.html',
        burner=burner,
        exceptionMessages=worker.exceptionMsg,
        pageBody="Index page.")


@app.route('/statistics')
def statistics():
    try:
        return render_template('statistics.html')
    except Exception as ex:
        return ex.message


@app.route('/simulator')
def simulator():
    try:
        return render_template('simulator.html')
    except Exception as ex:
        return ex.message


@app.route('/messages.read.status')
def messages():
    try:
        return flask.jsonify(errors=worker.exceptionMsg, status=burner.StatusMsg, fireWatch=burner.FireWatchLastValue)
    except Exception as ex:
        return ex

if __name__ == '__main__':
    app.run(host='0.0.0.0')
