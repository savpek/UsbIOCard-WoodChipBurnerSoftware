'use strict';

var burnerApp = angular.module('burnerApp', ['ngResource', 'ngRoute']);

burnerApp.config(function ($routeProvider) {
    $routeProvider.when('/settings', {templateUrl: 'partials/settings.html', controller: 'BurnerSettingsController'});
    $routeProvider.when('/iolog', {templateUrl: 'partials/iolog.html', controller: 'IoLogController'});
    $routeProvider.when('/statistics', {templateUrl: 'partials/statistics.html', controller: 'BurnerSettingsController'});
    $routeProvider.otherwise({redirectTo: '/settings'});
});

