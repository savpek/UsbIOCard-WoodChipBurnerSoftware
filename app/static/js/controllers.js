'use strict';

var controllers = {};
controllers.BurnerSettingsController = function ($scope, BurnerSettingsApiFactory) {
    var settings = BurnerSettingsApiFactory;

    settings.get({}, function(settings) {
        $scope.ScrewTimeInSeconds = settings.screwSec;
        $scope.DelayTimeInSeconds = settings.delaySec;
        $scope.CurrentFireLimit = settings.lightSensor;
        $scope.IsEnabled = settings.isEnabled;
    });

    $scope.updateSettings = function () {
        settings.update({
            screwSec: $scope.ScrewTimeInSeconds,
            delaySec: $scope.DelayTimeInSeconds,
            lightSensor: $scope.CurrentFireLimit,
            isEnabled: $scope.IsEnabled
        });
    };
};

burnerApp.controller(controllers);