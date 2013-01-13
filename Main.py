# coding=utf-8
from flask import Flask, render_template, request, jsonify
from Burner.Burner import Burner
from Burner.BurnerProcess import BurnerProcess
from Burner.IO.UsbCardSimulator import UsbCardSimulator

app = Flask(__name__)

def get_burner_process():
    ioCard = UsbCardSimulator("/dev/ttyUSB0", 9600)  # Define configurations for used IO card port.

    burner = Burner(ioCard, ScrewTerminal="2.T2", FanTerminal="2.T1", FireWatchTerminal="7.T0.ADC0")

    burnerProcess = BurnerProcess(burner)
    return burnerProcess

burnerProcess = get_burner_process()
burnerProcess.start()

@app.route('/')
def index():
    try:
        burnerProcess.ScrewSec = _get_float('ScrewTime', burnerProcess.ScrewSec)
        burnerProcess.DelaySec = _get_float('Delay', burnerProcess.DelaySec)
        burnerProcess.FireLimit = _get_float('FireWatch', burnerProcess.FireLimit)
        burnerProcess.Enabled = request.args.get('enabled', burnerProcess.Enabled) in ("True", True)
        return render_template('settings.html', burnerProcess=burnerProcess)
    except Exception, e:
        return e

def _get_float(name, default):
    try:
        return float(request.args.get(name, default))
    except ValueError:
        return default

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
        return jsonify(enabled=burnerProcess.Enabled, status=burnerProcess.StatusMsg, fireWatch=burnerProcess.get_fire_value())
    except Exception as ex:
        return ex


@app.route('/messages.read.simulator')
def simulator_read():
    try:
        return jsonify(iocard_log=BurnerProcess._controller._ioCard.Log)
    except Exception as ex:
        return ex

if __name__ == '__main__':
    app.run(host='0.0.0.0')
