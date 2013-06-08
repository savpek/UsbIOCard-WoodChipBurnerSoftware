'use strict';


var burnerApp = angular.module('burnerApp', ['ngResource', 'ui.bootstrap']);

burnerApp.config(function ($routeProvider) {
    $routeProvider.when('/settings', {templateUrl: 'static/partials/settings.html', controller: 'BurnerSettingsController'});
    $routeProvider.when('/simulator', {templateUrl: 'static/partials/simulator.html', controller: 'BurnerSettingsController'});
    $routeProvider.when('/statistics', {templateUrl: 'static/partials/statistics.html', controller: 'BurnerSettingsController'});
    $routeProvider.otherwise({redirectTo: '/settings'});
  });

