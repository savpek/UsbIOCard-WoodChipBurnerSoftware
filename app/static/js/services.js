'use strict';

var factories = {};

factories.BurnerSettingsApiFactory = function($resource) {
    var factory = $resource('/rest/settings', {}, {
        get: {method:"GET"},
        update: {method:"PUT"},
        isArray:false
    });
    return factory;
};


burnerApp.factory(factories);