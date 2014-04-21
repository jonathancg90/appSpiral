angular.module('modelApp').factory('ModelFactory', ['$http', function($http) {
    var self = this,
        factory = {};
    self.profile = {};


    factory.setModel = function(data){
        self.profile.name = data.name;
        self.profile.last_name = data.last_name;
        self.profile.type_doc = data.type_doc;
        self.profile.num_doc = data.num_doc;
        self.profile.address = data.address;
        self.profile.email = data.email;
        self.profile.birth = data.birth;
        self.profile.nationality = data.nationality;
    };

    factory.getCountries = function(urlCountries){
        return $http.get(urlCountries, { cache: true })
            .then(function(response) {
                if(response.data.status == 200) {
                    return response.data.countries;
                }
            });
    };

    factory.saveProfileData = function(urlSave, data){
        return $http.post(urlSave, angular.toJson(data))
            .then(function(response) {
                if(response.data.status == 200) {
                    return response.data.message;
                }
            });
    };

    factory.saveFeatureData = function(urlSave){
        return $http.post(urlSave, angular.toJson(self.profile))
            .then(function(response) {
                if(response.data.status == 200) {
                    return response.data.message;
                }
            });
    };

    factory.searchModel = function(urlSearch){
        return $http.get(urlSearch, { cache: true })
            .then(function(response) {
                if(response.status == 200) {
                    return response.data.profile;
                }
            });
    };

    return factory;
}]);