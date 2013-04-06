'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('myApp.services', [], function ($provide) {
    $provide.factory("baari", [function () {
        var baari = $.connection.bar;
        $.connection.hub.start();
        return baari;
    }]);
});


