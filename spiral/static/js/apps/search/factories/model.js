angular.module('searchApp').factory('ModelFactory',['$http', function($http) {
    var factory = {};

    factory.basicSearch = function(urlBasic, data){
        return $http.post(urlBasic, data)
            .then(function(response) {
                if(response.status == 200) {
                    return response.data;
                }else {
                   return [];
                }
            });
    };

    factory.advanceSearch = function(urlAdvance){

    };

    return factory;
}]);