'use strict';

var factories = {};

factories.BurnerApiFactory = function($resource) {
    var factory = $resource('/get/settings', {}, {
        get: {method:"GET"}, isArray:false});
    return factory;
};

burnerApp.factory(factories);