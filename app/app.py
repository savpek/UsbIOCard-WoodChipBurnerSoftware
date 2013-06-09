from flask import Flask, render_template, request, Response
from flask.ext import restful
from flask.ext.restful.reqparse import RequestParser

import werkzeug.serving
from gevent import monkey
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.server import SocketIOServer
from burner.burner import Burner
from burner.burnercontroller import BurnerController
from burner.burnerprocess import BurnerProcess
from burner.usbcard_simulator import UsbCardSimulator


iocard = UsbCardSimulator("/dev/ttyUSB0", 9600)  # Define configurations for used IO card port.

def get_burner_process(ioCard):
    burner = Burner(ioCard, ScrewTerminal="2.T2", FanTerminal="2.T1", FireWatchTerminal="7.T0.ADC0")
    burnerController = BurnerController(burner)
    burnerProcess = BurnerProcess(burnerController)

    # Initial values ...
    burnerProcess.ScrewSec = 1
    burnerProcess.DelaySec = 4
    return burnerProcess


app = Flask(__name__)
app.debug = True
monkey.patch_all()
restApi = restful.Api(app)

burnerProcess = get_burner_process(iocard)
burnerProcess.start()


class SettingsRestApi(restful.Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('screwSec', required=True, location='json', type=int)
        self.parser.add_argument('delaySec', required=True, location='json', type=int)
        self.parser.add_argument('lightSensor', required=True, location='json', type=int)
        self.parser.add_argument('isEnabled', required=True, location='json', type=bool)

    def get(self):
        return {'screwSec': burnerProcess.ScrewSec,
                'delaySec': burnerProcess.DelaySec,
                'lightSensor': burnerProcess.LightSensor,
                'isEnabled': burnerProcess.Enabled}

    def put(self):
        args = self.parser.parse_args()
        burnerProcess.ScrewSec = args['screwSec']
        burnerProcess.DelaySec = args['delaySec']
        burnerProcess.LightSensor = args['lightSensor']
        burnerProcess.Enabled = args['isEnabled']
        return args, 201


restApi.add_resource(SettingsRestApi, '/rest/settings')


@app.route("/")
def hello():
    return render_template("index.html")

class IoLogSpace(BaseNamespace):
    sockets = {}

    def recv_connect(self):
        self.sockets[id(self)] = self

    def disconnect(self, *args, **kwargs):
        if id(self) in self.sockets:
            del self.sockets[id(self)]
        super(IoLogSpace, self).disconnect(*args, **kwargs)

    @classmethod
    def broadcast(cls, event, message):
        for ws in cls.sockets.values():
            ws.emit(event, message)

@app.route('/socket.io/<path:rest>')
def push_stream(rest):
    socketio_manage(request.environ, {'/sockets': IoLogSpace}, request)
    return Response()

def log_messenger(message):
    IoLogSpace.broadcast('message', message)

burnerProcess.ErrorOccurredEvent = log_messenger
iocard.CardActionInvoked = log_messenger

def run_dev_server():
    app.debug = True
    port = 6020
    SocketIOServer(('', port), app, resource="socket.io").serve_forever()


if __name__ == "__main__":
    run_dev_server()


