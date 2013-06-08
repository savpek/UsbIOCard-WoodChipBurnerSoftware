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
    return {
        restrict: 'E',
        template: '<input type="button" ng-click="toggle()" class="{{buttonClass}}">ToggleButton</input>',
        scope: {},
        replace: false,
        controller: ['$scope', '$element', '$attrs', '$transclude', function ($scope, $element, $attrs, $transclude) {
            $scope.toggleValue = false;
            $scope.buttonClass = "btn btn-success";
        }],
        link: function (scope, elem, attrs) {
            scope.$watch('toggleValue', function (oldValue, newValue) {
                if(newValue) {
                    scope.buttonClass = "btn btn-success";
                }
                else {
                    scope.buttonClass = "btn btn-failure";
                }
            });

            scope.toggle = function () {
                scope.toggleValue = !scope.toggleValue;
            };
        }
    };
};

burnerApp.directive(directives);