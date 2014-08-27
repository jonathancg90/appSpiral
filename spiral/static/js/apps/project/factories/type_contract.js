projectApp.factory('typeContractFactory',['$http', function($http) {
    var factory = {};

    factory.save = function(urlSave, data){
        return $http.post(urlSave, angular.toJson(data))
            .then(function(response) {
                if(response.status == 200) {
                    return response.data;
                } else {
                    return [];
                }
            });
    };

    return factory;
}]);