'use strict';

var controllers = {};
controllers.BurnerSettingsController = function ($scope, BurnerSettingsApiFactory, Sockets) {
    var settings = BurnerSettingsApiFactory;

    settings.get({}, function(settings) {
        $scope.screwSec = settings.screwSec;
        $scope.delaySec = settings.delaySec;
        $scope.lightSensor = settings.lightSensor;
        $scope.isEnabled = settings.isEnabled;
    });

    $scope.updateSettings = function () {
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

    sockets.on('message', function (message) {
        console.log("Got message:", message);
        $scope.ioLog.unshift(message);

        if($scope.ioLog.length > 30) {
            $scope.ioLog.pop();
        }
    });
};

burnerApp.controller(controllers);