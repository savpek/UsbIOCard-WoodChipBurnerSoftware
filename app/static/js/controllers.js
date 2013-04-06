'use strict';

function ChangeSettingsController($scope, BurnerSettings) {
    $scope.currentLightSensorValue = "-";

    BurnerSettings.get(function(results) {
        $scope.screwDelay = results.DelayTimeInSeconds;
        $scope.screwTime = results.ScrewTimeInSeconds;
        $scope.lightSensorLimit = results.CurrentFireLimit;
    });

    $scope.save = function () {
    };
}
ChangeSettingsController.$inject = ['$scope', 'BurnerSettings'];