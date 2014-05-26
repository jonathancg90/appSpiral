angular.module('searchApp').service('detailService',['$http', function($http){
    var self = this;
    self.detail = [];

    self.getDetail = function(urlDetail, model_id) {
        return $http.get(urlDetail.replace(':pk', model_id))
            .then(function(response) {
                if(response.status == 200) {
                    return response.data;
                }else {
                    return {
                        'message':'ERR03: Ocurrio un error: notificar a soporte',
                        type: 'error'
                    };
                }
            });
    };
}]);
