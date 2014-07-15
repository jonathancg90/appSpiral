projectApp.factory('commercialFactory',['$http', function($http) {
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

    factory.saveCommercial = function(urlSave, data) {
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