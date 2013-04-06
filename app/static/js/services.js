'use strict';

angular.module('myApp.services', ['ngResource']).
    factory('BurnerSettings', function($resource){
        return $resource('/get/settings', { },{
                'get' : { method: 'GET', isArray : false }
        })
});

angular.module('myApp.services', ['ngResource']).
    factory('SimulatorValues', function($resource){
        return $resource('/get/simulator', { },{
            'get' : { method: 'GET', isArray : false }
        })
    });