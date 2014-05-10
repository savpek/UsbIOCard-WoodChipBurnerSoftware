var assert = require("assert");

var burnerPortApi = function(port, error, result) {
    var commands = {
        "FAN_ENABLE" : "SET 2.T2 HIGH",
        "FAN_DISABLE" : "SET 2.T2 LOW",
        "SCREW_ENABLE" : "SET 2.T1 HIGH",
        "SCREW_DISABLE" : "SET 2.T1 LOW"
    };

    var self = this;

    var serialPort = require("serialport");
    var driver = serialPort.SerialPort;

    var port = new driver("COM3", { baudrate: 9600,
        parser: serialPort.parsers.readline("\n")
    }, false);

    self.call = function(command) {
        port.open(function(){
            port.on('data', function (data) {
                console.log('Received from IO-card: ' + data);

                var response = { 'command' : command, 'response': data }
                result(response)
            });

            console.log('Writing to IO-card: ' + commands[command])
            port.write(commands[command]+"\n", function(err, result) {
                if(err) {
                    error(err)
                }
            })
        });
    }
    return self;
};

describe('Testers: IO card connectivity', function() {
    it('Enable screw relay.', function (done) {
        var port = burnerPortApi("COM3", function(err) {
            done();
        },
        function (data) {
            done();
        });

        port.call("SCREW_ENABLE");
    });

    it('Read light meter value.', function() {
    });
});