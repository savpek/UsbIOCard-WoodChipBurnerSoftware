'use strict';

var directives = {};

directives.helloWorld = function () {
    return {
            restrict: 'A',
            link: function postLink (scope, iElement, iAttrs, controller) {
                var foo = 3;
            }
        };
};

directives.toggleButton = function () {
    var buttonOff = function(scope) {
        scope.buttonClass = "btn btn-danger";
        scope.buttonText = "Off";
    };

    var buttonOn = function(scope) {
        scope.buttonClass = "btn btn-success";
        scope.buttonText = "On";
    };

    var directive = {
        restrict: 'E',
        template: '<input type="button" ng-click="toggle()" class="{{buttonClass}}" value="{{buttonText}}" />',
        scope: {
            toggleValue: '@variable'
        },
        replace: true,
        controller: ['$scope', '$element', '$attrs', '$transclude', function ($scope, $element, $attrs, $transclude) {
            $scope.toggleValue = false;
            buttonOff($scope);
        }],
        link: function (scope) {
            scope.$watch('toggleValue', function () {
                if (scope.toggleValue) {
                    buttonOn(scope);
                }
                else {
                    buttonOff(scope);
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