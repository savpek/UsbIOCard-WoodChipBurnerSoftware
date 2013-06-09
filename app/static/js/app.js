'use strict';

var burnerApp = angular.module('burnerApp', ['ngResource']);

burnerApp.config(function ($routeProvider) {
    $routeProvider.when('/settings', {templateUrl: 'static/partials/settings.html', controller: 'BurnerSettingsController'});
    $routeProvider.when('/iolog', {templateUrl: 'static/partials/iolog.html', controller: 'IoLogController'});
    $routeProvider.when('/statistics', {templateUrl: 'static/partials/statistics.html', controller: 'BurnerSettingsController'});
    $routeProvider.otherwise({redirectTo: '/settings'});
});

