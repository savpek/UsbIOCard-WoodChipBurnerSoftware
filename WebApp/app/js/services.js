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

factories.Sockets = function ($rootScope) {
    /*
    var socket = io.connect('/sockets');
    var factory = {
        on: function (eventName, callback) {
            socket.on(eventName, function () {
                var args = arguments;
                $rootScope.$apply(function () {
                    callback.apply(socket, args);
                });
            });
        },
        emit: function (eventName, data, callback) {
            socket.emit(eventName, data, function () {
                var args = arguments;
                $rootScope.$apply(function () {
                    if (callback) {
                        callback.apply(socket, args);
                    }
                });
            });
        }
    };*/
    return factory;
};
burnerApp.factory(factories);