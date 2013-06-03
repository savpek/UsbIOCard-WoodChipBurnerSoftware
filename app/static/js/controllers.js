'use strict';

var controllers = {};
controllers.BurnerSettingsController = function ($scope, BurnerSettingsApiFactory) {
    BurnerSettingsApiFactory.get({}, function(settings) {
        $scope.screwDelay = settings.DelayTimeInSeconds;
        $scope.screwTime = settings.ScrewTimeInSeconds;
        $scope.lightSensorLimit = settings.CurrentFireLimit;
        $scope.isEnabled = settings.isEnabled;
    });

    $scope.updateSettings = function() {
        BurnerSettingsApiFactory.get({}, function(settings) {
            $scope.screwDelay = settings.DelayTimeInSeconds;
            $scope.screwTime = settings.ScrewTimeInSeconds;
            $scope.isEnabled = settings.isEnabled;
        });
    }
};

burnerApp.controller(controllers);