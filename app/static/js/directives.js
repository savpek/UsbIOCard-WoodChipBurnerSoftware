'use strict';

var directives = {};

directives.toggleButton = function () {
    var directive = {
        restrict: 'E',
        template: '<input type="button" ng-click="toggle()" class="{{buttonClass}}" value="{{buttonText}}" />',
        scope: {
            toggleValue:'=forVariable'
        },
        replace: true,
        link: function (scope) {
            var buttonOff = function () {
                scope.buttonClass = "btn btn-danger";
                scope.buttonText = "Off";
            };

            var buttonOn = function () {
                scope.buttonClass = "btn btn-success";
                scope.buttonText = "On";
            };

            scope.toggleValue = false;
            buttonOff(scope);

            scope.$watch('toggleValue', function () {
                if (scope.toggleValue) {
                    buttonOn();
                }
                else {
                    buttonOff();
                }
            });

            scope.toggle = function () {
                scope.toggleValue = !scope.toggleValue;
            };
        }
    };

    return directive;
};

burnerApp.directive(directives);