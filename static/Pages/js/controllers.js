'use strict';

function ChatPageController($rootScope, baari) {
    $rootScope.currentMessage = "";
    $rootScope.firstName = "Name";

    $rootScope.messages = [];

    baari.client.addMessage = function (message) {
        $rootScope.messages.unshift(message);

        if ($rootScope.messages.length > 10)
            $rootScope.messages.pop();
            
        $rootScope.$digest();
    };

    $rootScope.send = function () {
        if ($rootScope.firstName == "" || $rootScope.currentMessage == "")
            return;
        
        baari.server.send($rootScope.currentMessage, $rootScope.firstName);

        $rootScope.currentMessage = "";
    };
}
ChatPageController.$inject = ['$rootScope', "baari"];