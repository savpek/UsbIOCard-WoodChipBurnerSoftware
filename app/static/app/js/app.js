'use strict';

// Declare app level module which depends on filters, and services
angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives', 'myApp.controllers']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/view1', {templateUrl: 'static/app/partials/partial1.html', controller: 'BurnerControl'});
    $routeProvider.when('/view2', {templateUrl: 'static/app/partials/partial2.html', controller: 'BurnerControl'});
    $routeProvider.otherwise({redirectTo: '/view1'});
  }]);
