'use strict';

var controllers = {};


controllers.BurnerSettingsController = function ($scope, BurnerSettingsApiFactory, Sockets) {
    var settings = BurnerSettingsApiFactory;
    var sockets = Sockets;

    sockets.on('error', function (message) {
            if ($scope.error === undefined) {
                $scope.isEnabled = false;
            }
            $scope.error = message;
        });

    sockets.on('lightSensorMeasured', function (message) {
            $scope.lightSensorMeasured = message;
        });

    settings.get({}, function(settings) {
        $scope.screwSec = settings.screwSec;
        $scope.delaySec = settings.delaySec;
        $scope.lightSensor = settings.lightSensor;
        $scope.isEnabled = settings.isEnabled;
    });

    $scope.updateSettings = function () {
        $scope.error = undefined;

        settings.update({
            screwSec: $scope.screwSec,
            delaySec: $scope.delaySec,
            lightSensor: $scope.lightSensor,
            isEnabled: $scope.isEnabled
        });
    };
};

controllers.IoLogController = function ($scope, Sockets) {
    var sockets = Sockets;
    $scope.ioLog = [];

    sockets.on('iolog', function (message) {
        $scope.ioLog.unshift(message);

        if($scope.ioLog.length > 30) {
            $scope.ioLog.pop();
        }
    });
};

burnerApp.controller(controllers);