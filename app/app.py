# coding=utf-8
from flask import Flask, render_template, json, request
from flask.ext import restful
from flask.ext.restful.reqparse import RequestParser
from factories import get_burner_process

app = Flask(__name__)
restApi = restful.Api(app)

burnerProcess = get_burner_process()
burnerProcess.start()


class SimulatorRestApi(restful.Resource):
    def get(self):
        return {'FanState': burnerProcess._controller._burner._ioCard.FanState,
                'ScrewState': burnerProcess._controller._burner._ioCard.ScrewState}

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api')
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            message = ws.wait()
            ws.send(message)
    return

restApi.add_resource(SimulatorRestApi, '/rest/simulator')
restApi.add_resource(SettingsRestApi, '/rest/settings')

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

server = pywsgi.WSGIServer(("", 5000), app,
    handler_class=WebSocketHandler)
server.serve_forever()