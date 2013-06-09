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


def get_burner_process():
    ioCard = UsbCardSimulator("/dev/ttyUSB0", 9600)  # Define configurations for used IO card port.
    burner = Burner(ioCard, ScrewTerminal="2.T2", FanTerminal="2.T1", FireWatchTerminal="7.T0.ADC0")
    burnerController = BurnerController(burner)
    burnerProcess = BurnerProcess(burnerController)

    # Initial values ...
    burnerProcess.ScrewSec = 1
    burnerProcess.DelaySec = 4
    return burnerProcess

app = Flask(__name__)
monkey.patch_all()
restApi = restful.Api(app)

burnerProcess = get_burner_process()
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
                'delaySec' : burnerProcess.DelaySec,
                'lightSensor' : burnerProcess.LightSensor,
                'isEnabled' :burnerProcess.Enabled}

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

class ShoutsNamespace(BaseNamespace):
    sockets = {}
    def recv_connect(self):
        print "Got a socket connection" # debug
        self.sockets[id(self)] = self
    def disconnect(self, *args, **kwargs):
        print "Got a socket disconnection" # debug
        if id(self) in self.sockets:
            del self.sockets[id(self)]
        super(ShoutsNamespace, self).disconnect(*args, **kwargs)
    # broadcast to all sockets on this channel!
    @classmethod
    def broadcast(self, event, message):
        for ws in self.sockets.values():
            ws.emit(event, message)


@app.route('/socket.io/<path:rest>')
def push_stream(rest):
    try:
        socketio_manage(request.environ, {'/shouts': ShoutsNamespace}, request)
    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()

@app.route("/shout", methods=["GET"])
def say():
    message = request.args.get('msg', None)
    if message:
        ShoutsNamespace.broadcast('message', message)
        return Response("Message shouted!")
    else:
        return Response("Please specify your message in the 'msg' parameter")

def bar():
    ShoutsNamespace.broadcast('message', "LOLLEROO")

burnerProcess.Foo = bar

@werkzeug.serving.run_with_reloader
def run_dev_server():
    app.debug = True
    port = 6020
    SocketIOServer(('', port), app, resource="socket.io").serve_forever()

if __name__ == "__main__":
    run_dev_server()


