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

directives.fundooRating = function () {
    return {
      restrict: 'A',
      link: function (scope, elem, attrs) {
        console.log("Recognized the fundoo-rating directive usage");
      }
    };
};

/* global burnerApp */
burnerApp.directive(directives);