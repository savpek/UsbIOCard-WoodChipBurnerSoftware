var assert = require("assert");

var com = "COM3"

var serialPortApi = function(port) {
    var self = this;

    var driver = require("serialport").SerialPort;
    var port = new driver(port, { baudrate: 9600 }, false);

    self.Write = function (command, success, error) {
        port.open(function (){
            port.write(command, function(err, result) {
                console.log("error: " + err);
                console.log("result: " + result)
            })
        });
    }
    return self;
};

describe('Testers: IO card responds', function() {
    it('When reset watchdog is called, return ok.', function(done) {
        var serialPort = require("serialport");
        var driver = serialPort.SerialPort;

        var port = new driver("COM3", { baudrate: 9600,
            parser: serialPort.parsers.readline("\n")
        }, false);

        port.open(function (){
            console.log("open");
            port.on('data', function(data) {
                console.log('data received: ' + data);
                done();
            });
            port.write("testi\n", function(err, result) {
                console.log(err)
            })
        });
    });

    /*
    it('When reset watchdog is called, return ok. 2', function(done) {
        var serialPort = require("serialport");
        serialPort.list(function (err, ports) {
            ports.forEach(function(port) {
                console.log(port.comName);
                console.log(port.pnpId);
                console.log(port.manufacturer);
            });
            done();
        });
    });
    */
});