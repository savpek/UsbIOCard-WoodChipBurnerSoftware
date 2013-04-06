'use strict';

angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('#test', {templateUrl: 'partial/settings.html', controller: ChangeSettingsController});
    $routeProvider.otherwise({redirectTo: '#test'});
  }]);