var IOCard = function(portOpenedCallback) {
    var commands = {
        "FAN_ENABLE" : "SET 2.T2 HIGH",
        "FAN_DISABLE" : "SET 2.T2 LOW",
        "SCREW_ENABLE" : "SET 2.T1 HIGH",
        "SCREW_DISABLE" : "SET 2.T1 LOW",
        "READ_LIGHTMETER" : "ADC 7.T0.ADC0"
    };

    var usableApi = {};

    var responseCallBack = function(response) {};
    var errorCallBack = function(error) {};

    var serialPortFactory = require("serialport");

    var serialPort = new serialPortFactory.SerialPort("COM3", { baudrate: 9600,
        parser: serialPortFactory.parsers.readline("\n")
    });

    usableApi.on = function(action, callback) {
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
        portOpenedCallback(usableApi)
    });

    serialPort.on('error', function(err) {
        console.log("Seriaport raised error: " + err);
    });

    serialPort.on('close', function() {
        console.log("Serialport closed.")
    });

    serialPort.on('data', function (data) {
        console.log('Received from IO-card: ' + data);

        if (data.indexOf("ERROR") > -1) {
            errorCallBack("Received error from io card, message: " + data);
            return;
        }

        var response = { 'response': data.replace('\r', '').replace('\n', ''), 'isEcho': false };

        for(var key in commands) {
            if (data.indexOf(commands[key]) > -1) {
                response.isEcho = true;
            }
        }

        console.log("Response: ", response);
        responseCallBack(response)
    });

    usableApi.write = function(command) {
        if(!commands[command]) {
            console.log("Invalid parameter given for call, returning.");
            errorCallBack("Invalid command parameter for IO card, invalid command was '" + command + "'");
            return;
        }

        console.log('Writing to IO-card: ' + commands[command]);
        serialPort.write(commands[command] + "\n");
    };
    return this;
};

describe('Testers: IO card connectivity', function() {
    this.timeout(10000);

    it('Test card communication.', function (done) {
        setTimeout(done, 1000);
        IOCard(function(io) {
            io.on('response', function(data) {
            });

            io.on('error', function(error) {
                throw "Failed, reason: " + error;
            });
            io.write("SCREW_ENABLE");
            io.write("READ_LIGHTMETER");
        });
    });
});