'use strict';

function ChangeSettingsController($scope, BurnerSettings) {
        $scope.currentLightSensorValue = "-";

        BurnerSettings.get = function(results) {
            $scope.screwDelay = results.DelayTimeInSeconds;
            $scope.screwTime = results.ScrewTimeInSeconds;
            $scope.lightSensorLimit = results.CurrentFireLimit;
        });

        $scope.save = function () {
        };
    }
    ChangeSettingsController.$inject = ['$scope', 'BurnerSettings'];

function SimulatorController($scope, SimulatorValues) {
    SimulatorValues.get(function(results) {
        $scope.simulatedLightSensorValue = results.DelayTimeInSeconds;
        $scope.screwState = results.FanState;
        $scope.fanState = results.ScrewState;
    });

    $scope.save = function () {
    };
}
SimulatorController.$inject = ['$scope', 'SimulatorValues'];

