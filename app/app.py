# coding=utf-8
from flask import Flask, render_template, json, request
from flask.ext import restful
from flask.ext.restful.reqparse import RequestParser
from factories import get_burner_process

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

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
def index():
    return render_template('index.html')


def my_app(environ, start_response):
    path = environ["PATH_INFO"]
    if path == "/websocket":
        handle_websocket(environ["wsgi.websocket"])
    else:
        return app(environ, start_response)


def handle_websocket(ws):
    while True:
        message = ws.receive()
        if message is None:
            break
        else:
            message = json.loads(message)

            r  = "I have received this message from you : %s" % message
            r += "<br>Glad to be your webserver."
            ws.send(json.dumps({'output': r}))


restApi.add_resource(SimulatorRestApi, '/rest/simulator')
restApi.add_resource(SettingsRestApi, '/rest/settings')


if __name__ == '__main__':
    http_server = WSGIServer(('',5000), my_app, handler_class=WebSocketHandler)
    http_server.serve_forever()