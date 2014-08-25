projectApp.factory('projectFactory',['$http', function($http) {
    var factory = {};

    factory.searchUrl = function(urlSearch){
        return $http.get(urlSearch)
            .success(function(response) {
                if(response.status == 200) {
                    return response.data;
                } else {
                    return [];
                }
            }).error(function (err, status) {

            });
    };
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

    factory.searchPost = function(urlSearch, data){
        return $http.post(urlSearch, angular.toJson(data))
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