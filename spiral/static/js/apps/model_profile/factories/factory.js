angular.module('modelApp').factory('ModelFactory', ['$http', function($http) {
    var self = this,
        factory = {};
    self.profile = {};


    factory.setProfile = function(data){
        self.profile.name_complete = data.name_complete;
        self.profile.type_doc = data.type_doc;
        self.profile.num_doc = data.num_doc;
        self.profile.address = data.address;
        self.profile.email = data.email;
        self.profile.birth = data.birth;
        self.profile.nationality = data.nationality.id;
        self.profile.city = data.city.city_id;
        self.profile.phone_fixed = data.phone_fixed;
        self.profile.phone_mobil = data.phone_mobil;
        self.profile.address = data.address;
        self.profile.gender = data.gender.id;
        self.profile.height = data.height;
        self.profile.weight = data.weight;
    };

    factory.getCountries = function(urlCountries){
        return $http.get(urlCountries, { cache: true })
            .then(function(response) {
                if(response.data.status == 200) {
                    return response.data.countries;
                }
            });
    };

    factory.saveProfileData = function(urlSave){
        return $http.post(urlSave, angular.toJson(self.profile))
            .then(function(response) {
                if(response.status == 200) {
                    return response.data
                } else{
                    return {
                        'status':'error',
                        'message':'ERR02: Ocurrio un error: notificar a soporte'
                    };
                }
            });
    };

    factory.saveFeatureData = function(urlSave, data){
        return $http.post(urlSave, angular.toJson(data))
            .then(function(response) {
                if(response.status == 200) {
                    return response.data;
                }
            });
    };

    factory.updateFeatureData = function(urlUpdate, data){
        return $http.post(urlUpdate, angular.toJson(data))
            .then(function(response) {
                if(response.status == 200) {
                    return response.data;
                }
            });
    };

    factory.deleteFeatureData = function(urlDelete, data){
        return $http.post(urlDelete, angular.toJson(data))
            .then(function(response) {
                if(response.status == 200) {
                    return response.data;
                }
            });
    };

    factory.searchModel = function(urlSearch){
        return $http.get(urlSearch, { cache: true })
            .then(function(response) {
                if(response.status == 200) {
                    return response.data;
                } else {
                    return {
                        'message':'ERR01: Ocurrio un error: notificar a soporte',
                        type: 'error'
                    };
                }
            });
    };

    return factory;
}]);