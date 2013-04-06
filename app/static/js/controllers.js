'use strict';

function ChangeSettingsController($scope) {
    $scope.currentValue = 100;
    $scope.lightSensorLimit = 50;

    $scope.messages = [];

    $scope.save = function () {

    };
}
ChangeSettingsController.$inject = ['$scope'];