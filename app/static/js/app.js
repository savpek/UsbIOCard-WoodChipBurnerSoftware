'use strict';

var burnerApp = angular.module('burnerApp', ['ngResource', 'ui.bootstrap']);

burnerApp.config(function ($routeProvider) {
    $routeProvider.when('/test', {templateUrl: 'static/partials/settings.html', controller: 'BurnerSettingsController'});
    $routeProvider.otherwise({redirectTo: '/test'});
  });