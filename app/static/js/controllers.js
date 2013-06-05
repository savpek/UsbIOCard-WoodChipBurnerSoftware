'use strict';

var controllers = {};
controllers.BurnerSettingsController = function ($scope, BurnerSettingsApiFactory) {
    BurnerSettingsApiFactory.get({}, function(settings) {
        $scope.DelayTimeInSeconds = settings.DelayTimeInSeconds;
        $scope.ScrewTimeInSeconds = settings.ScrewTimeInSeconds;
        $scope.CurrentFireLimit = settings.CurrentFireLimit;
        $scope.IsEnabled = settings.IsEnabled;
    });

    $scope.updateSettings = function() {
        BurnerSettingsApiFactory.update({
            ScrewTimeInSeconds: $scope.ScrewTimeInSeconds,
            DelayTimeInSeconds: $scope.DelayTimeInSeconds,
            CurrentFireLimit: $scope.CurrentFireLimit,
            IsEnabled: $scope.IsEnabled
        });
    }
};

burnerApp.controller(controllers);