projectApp.factory('projectFactory',['$http', function($http) {
    var factory = {};

    factory.searchUrl = function(urlSearch){
        return $http.get(urlSearch)
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