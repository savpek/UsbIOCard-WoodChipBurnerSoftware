# coding=utf-8
import threading
from flask import Flask, render_template, request
import time
import flask
from Burner import Burner
from UsbCard import UsbCard
from UsbCardSimulator import UsbCardSimulator

app = Flask(__name__)


def configure_burner():
    ioCard = UsbCardSimulator("/dev/ttyUSB0", 9600)  # Define configurations for used IO card port.

    burner = Burner(ioCard, time.sleep)

    burner.Delay = 10       # Default setting on startup.
    burner.ScrewTime = 2
    burner.FanTerminalName = "2.T1"     # Look these from IO card printout.
    burner.ScrewTerminalName = "2.T2"
    burner.FireWatchTerminalName = "7.T0.ADC0"
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


@app.route('/')
def index():
    burner.Enabled = request.args.get('enabled', burner.Enabled) in ("True", True)
    return render_template('settings.html')


@app.route('/statistics')
def statistics():
    try:
        return render_template('statistics.html', log=burner._ioCard.get_log_as_string())
    except Exception as ex:
        return ex.message


@app.route('/simulator')
def simulator():
    try:
        return render_template('simulator.html', log=burner._ioCard.Log)
    except Exception as ex:
        return ex.message


@app.route('/messages.read.status')
def messages():
    try:
        return flask.jsonify(errors=worker.exceptionMsg, status=burner.StatusMsg, fireWatch=burner.FireWatchLastValue)
    except Exception as ex:
        return ex


@app.route('/messages.read.simulator')
def simulator_read():
    try:
        return flask.jsonify(iocard_log=burner._ioCard.Log)
    except Exception as ex:
        return ex

if __name__ == '__main__':
    app.run(host='0.0.0.0')
