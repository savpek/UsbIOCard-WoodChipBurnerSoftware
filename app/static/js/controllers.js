'use strict';

var controllers = {};
controllers.BurnerSettingsController = function ($scope, BurnerApiFactory) {
    $scope.currentLightSensorValue = 33;
    $scope.updateSettings = function() {
        BurnerApiFactory.get({}, function(settings) {
            $scope.currentLightSensorValue = settings.ScrewTimeInSeconds;
        });
    }
};

burnerApp.controller(controllers);