projectApp.factory('clientFactory',['$http', function($http) {
    var factory = {};

    factory.all = function(urlSearch){
        return $http.get(urlSearch)
            .then(function(response) {
                if(response.status == 200) {
                    return response.data;
                }else {
                    return [];
                }
            });
    };

    factory.getTypeClients = function(urlSearch){
        return $http.get(urlSearch)
            .then(function(response) {
                if(response.status == 200) {
                    return response.data;
                }else {
                    return [];
                }
            });
    };

    factory.saveClient = function(urlSave, data){
        return $http.post(urlSave, angular.toJson(data))
            .then(function(response) {
                if(response.status == 200) {
                    return response.data;
                }else {
                    return [];
                }
            });
    };
    return factory;
}]);