'use strict';

var module = angular.module('myApp.services', ['ngResource']);

    module.
        factory('BurnerSettings', function($resource){
            return $resource('/get/settings', { },{
                    'get' : { method: 'GET', isArray : false }
            })();
    });


    module.
        factory('SimulatorValues', function($resource){
            return $resource('/get/simulator', { },{
                'get' : { method: 'GET', isArray : false }
            })();
        });
