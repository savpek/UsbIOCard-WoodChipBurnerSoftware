# coding=utf-8
from flask import Flask, render_template, jsonify
from flask.ext import restful
import parser
from Burner.Burner import Burner
from Burner.BurnerController import BurnerController
from Burner.BurnerProcess import BurnerProcess
from Burner.IO.UsbCardSimulator import UsbCardSimulator
from Burner.StatisticsProcess import StatisticsProcess

app = Flask(__name__)
app.config['DEBUG'] = True
restApi = restful.Api(app)


def get_burner_process():
    ioCard = UsbCardSimulator("/dev/ttyUSB0", 9600)  # Define configurations for used IO card port.
    burner = Burner(ioCard, ScrewTerminal="2.T2", FanTerminal="2.T1", FireWatchTerminal="7.T0.ADC0")
    burnerController = BurnerController(burner)
    burnerProcess = BurnerProcess(burnerController)
    burnerProcess.ScrewSec = 1
    burnerProcess.DelaySec = 4
    return burnerProcess


burnerProcess = get_burner_process()
burnerProcess.start()

statisticsProcess = StatisticsProcess(burnerProcess)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/messages.read.status')
def messages():
    return jsonify(enabled=burnerProcess.Enabled, status=burnerProcess.Status, fireWatch=burnerProcess.get_fire_value())


@app.route('/messages.read.simulator')
def simulator_read():
    return jsonify(
        Log=burnerProcess._controller._burner._ioCard.Log,
        FanState=burnerProcess._controller._burner._ioCard.FanState,
        ScrewState=burnerProcess._controller._burner._ioCard.ScrewState)


class SimulatorState(restful.Resource):
    def get(self):
        return {'FanState': burnerProcess._controller._burner._ioCard.FanState,
                'ScrewState': burnerProcess._controller._burner._ioCard.ScrewState}


class SettingsViaRest(restful.Resource):
    def get(self):
        return {'ScrewTimeInSeconds': burnerProcess.ScrewSec,
                'DelayTimeInSeconds' : burnerProcess.DelaySec,
                'CurrentFireLimit' : burnerProcess.FireLimit,
                'IsEnabled' :burnerProcess.Enabled}

    def put(self):
        args = parser.parse_args()
        burnerProcess.FireLimit = args['lightSensorLimit']
        burnerProcess.DelaySec = args['screwDelay']
        burnerProcess.DelaySec = args['screwTime']
        return '', 200


restApi.add_resource(SettingsViaRest, '/get/settings')
restApi.add_resource(SimulatorState, '/get/simulator')

if __name__ == '__main__':
    app.run()
