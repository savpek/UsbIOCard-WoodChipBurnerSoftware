# coding=utf-8
from flask import Flask, render_template
from flask.ext import restful
from flask.ext.restful.reqparse import RequestParser

# Cannot use flask internal web server due performance issues...
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
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

@app.route('/')
def home(any=None):
    return render_template('index.html')

restApi.add_resource(SimulatorRestApi, '/rest/simulator')
restApi.add_resource(SettingsRestApi, '/rest/settings')

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
