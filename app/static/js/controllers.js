'use strict';

var controllers = {};
controllers.BurnerSettingsController = function ($scope, BurnerSettingsApiFactory, Sockets) {
    var settings = BurnerSettingsApiFactory;
    var sockets = Sockets;

    sockets.on('message', function (message) {
        console.log("Got message:", message);
        $scope.jorma = message;
    });

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

burnerApp.controller(controllers);