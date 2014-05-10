var assert = require("assert");

var burnerPortApi = function(port) {
    var commands = {
        "FAN_ENABLE" : "SET 2.T2 HIGH",
        "FAN_DISABLE" : "SET 2.T2 LOW",
        "SCREW_ENABLE" : "SET 2.T1 HIGH",
        "SCREW_DISABLE" : "SET 2.T1 LOW",
        "READ_LIGHTMETER" : "READ SOMETHING"
    };

    var self = this;

    var serialPort = require("serialport");
    var driver = serialPort.SerialPort;

    var port = new driver("COM3", { baudrate: 9600,
        parser: serialPort.parsers.readline("\n")
    }, false);

    self.call = function(command, error, result) {
        port.open(function(){
            if(!commands[command]) {
                console.log("Invalid parameter given for call, returning.");
                error("Invalid command parameter for IO card, invalid command was'" + command + "'");
                return;
            }

            port.on('data', function (data) {
                console.log('Received from IO-card: ' + data);

                if(result) {
                    var response = { 'command' : command, 'response': data.replace('\r','').replace('\n',''), 'isEcho':false };

                    if(data.indexOf(commands[command]) > -1) {
                        response.isEcho = true;
                    }

                    console.log("Response:", response);
                    result(response)
                }
                else {
                    console.log("Result function not defined, nothing returned.")
                }
            });

            console.log('Writing to IO-card: ' + commands[command]);
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
    this.timeout(6000);

    it('Enable screw relay.', function (done) {
        setTimeout(done, 3000);
        var port = burnerPortApi("COM3");

        port.call("SCREW_ENABLE", function(err){}, function(res) {});
    });

    it('Invalid command should cause error.', function(done) {
        setTimeout(done, 3000);
        var port = burnerPortApi("COM3");

        port.call("INVALID_COMMAND_HERE", function(err) {
            console.log("Error received: " + err);
        }, function(result){
        });
    });
});