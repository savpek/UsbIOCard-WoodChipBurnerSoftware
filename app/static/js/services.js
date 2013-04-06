'use strict';

angular.module('myApp.services', ['ngResource']).
    factory('BurnerSettings', function($resource){
        var settings = $resource('/get/settings', { },{
                'get' : { method: 'GET', isArray : false }
        })

        return settings;
    });