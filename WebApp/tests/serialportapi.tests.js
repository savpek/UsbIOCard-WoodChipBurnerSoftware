var burnerPortApi = (function() {
    var commands = {
        "FAN_ENABLE" : "SET 2.T2 HIGH",
        "FAN_DISABLE" : "SET 2.T2 LOW",
        "SCREW_ENABLE" : "SET 2.T1 HIGH",
        "SCREW_DISABLE" : "SET 2.T1 LOW",
        "READ_LIGHTMETER" : "ADC 7.T0.ADC0"
    };

    var that = this;

    var responseCallBack = function(response) {};
    var errorCallBack = function(error) {};

    var serialPortFactory = require("serialport");

    var serialPort = new serialPortFactory.SerialPort("COM3", { baudrate: 9600,
        parser: serialPortFactory.parsers.readline("\n")
    }, false);

    that.on = function(action, callback) {
        switch (action) {
            case 'error':
                errorCallBack = callback;
                break;
            case 'response':
                responseCallBack = callback;
                break;
            default:
                console.log("Called on method with invalid action switch.");
                throw "Called on method with invalid action switch.";
        }
    };

    serialPort.on('open', function() {
        console.log("Serial port opened.");

        serialPort.on('close', function() {
            console.log("connection closed.")
        });

        serialPort.on('error', function(err) {
            console.log("vitunvittu." + err);
            throw "eivitunvittu " + err;
        });
    });

    that.write = function(command) {
        if(!commands[command]) {
            console.log("Invalid parameter given for call, returning.");
            errorCallBack("Invalid command parameter for IO card, invalid command was '" + command + "'");
            return;
        }

        serialPort.open(function() {
            serialPort.on('data', function (data) {
                console.log('Received from IO-card: ' + data);

                var response = { 'command': command, 'response': data.replace('\r', '').replace('\n', ''), 'isEcho': false };

                if (data.indexOf(commands[command]) > -1) {
                    response.isEcho = true;
                }

                console.log("Response: ", response);
                responseCallBack(response)
            });

            console.log('Writing to IO-card: ' + commands[command]);
            serialPort.write(commands[command] + "\n");
        });
    };

    return that;
})();

describe('Testers: IO card connectivity', function() {
    this.timeout(9000);

    it('Enable screw relay.', function (done) {
        setTimeout(done, 3000);
        burnerPortApi.write("SCREW_ENABLE");
    });

    it('Reading lightmeter returns value.', function(done) {
        setTimeout(done, 3000);
        burnerPortApi.write("READ_LIGHTMETER");
    });

    it('Invalid command should cause error.', function(done) {
        setTimeout(done, 3000);
        burnerPortApi.write("INVALID_COMMAND_HERE");
    });
});