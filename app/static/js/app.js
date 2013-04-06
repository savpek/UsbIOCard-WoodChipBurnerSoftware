'use strict';

angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/test', {templateUrl: 'static/partials/settings.html', controller: ChangeSettingsController});
    $routeProvider.when('/statistics', {templateUrl: 'static/partials/statistics.html', controller: ChangeSettingsController});
    $routeProvider.when('/simulator', {templateUrl: 'static/partials/simulator.html', controller: ChangeSettingsController});
    $routeProvider.otherwise({redirectTo: '/test'});
  }]);