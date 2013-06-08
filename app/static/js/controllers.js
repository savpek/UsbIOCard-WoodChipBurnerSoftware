'use strict';

var controllers = {};
controllers.BurnerSettingsController = function ($scope, BurnerSettingsApiFactory) {
    var settings = BurnerSettingsApiFactory;

    settings.get({}, function(settings) {
        $scope.DelayTimeInSeconds = settings.DelayTimeInSeconds;
        $scope.ScrewTimeInSeconds = settings.ScrewTimeInSeconds;
        $scope.CurrentFireLimit = settings.CurrentFireLimit;
        $scope.IsEnabled = settings.IsEnabled === "True";
    });

    $scope.updateSettings = function () {
        settings.update({
            ScrewTimeInSeconds: $scope.ScrewTimeInSeconds,
            DelayTimeInSeconds: $scope.DelayTimeInSeconds,
            CurrentFireLimit: $scope.CurrentFireLimit,
            IsEnabled: $scope.IsEnabled
        });
    };
};

burnerApp.controller(controllers);