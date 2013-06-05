# coding=utf-8
from flask import Flask, render_template, jsonify, request
from flask.ext import restful
from flask.ext.restful import reqparse
from flask.ext.restful.reqparse import RequestParser
from Burner.Burner import Burner
from Burner.BurnerController import BurnerController
from Burner.BurnerProcess import BurnerProcess
from Burner.IO.UsbCardSimulator import UsbCardSimulator
from Burner.StatisticsProcess import StatisticsProcess

app = Flask(__name__)
app.debug = False
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
def home():
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


class SettingsState(restful.Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('ScrewTimeInSeconds', required=True, location='json', type=int)
        self.parser.add_argument('DelayTimeInSeconds', required=True, location='json', type=int)
        self.parser.add_argument('CurrentFireLimit', required=True, location='json', type=int)
        self.parser.add_argument('IsEnabled', required=True, location='json')

    def get(self):
        return {'ScrewTimeInSeconds': burnerProcess.ScrewSec,
                'DelayTimeInSeconds' : burnerProcess.DelaySec,
                'CurrentFireLimit' : burnerProcess.FireLimit,
                'IsEnabled' :burnerProcess.Enabled}

    def put(self):
        args = self.parser.parse_args()
        burnerProcess.ScrewSec = args['ScrewTimeInSeconds']
        burnerProcess.DelaySec = args['DelayTimeInSeconds']
        burnerProcess.FireLimit = args['CurrentFireLimit']
        burnerProcess.Enabled = args['IsEnabled']
        return args, 201


restApi.add_resource(SimulatorState, '/rest/simulator')
restApi.add_resource(SettingsState, '/rest/settings')

if __name__ == '__main__':
    app.run(debug=True, port=12345)
