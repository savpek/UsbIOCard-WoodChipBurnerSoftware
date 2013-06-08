'use strict';

var controllers = {};
controllers.BurnerSettingsController = function ($scope, BurnerSettingsApiFactory) {
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

burnerApp.controller(controllers);