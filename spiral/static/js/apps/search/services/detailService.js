angular.module('searchApp').service('detailService',['$http', function($http){
    var self = this;
    self.detail = [];

    self.getDetail = function(model) {
        var basic = {};
        angular.copy(model, basic);
        self.data = {
            'photos': [
                {
                    'image': '',
                    'thumb': ''
                },
                {
                    'image': '',
                    'thumb': ''
                }
            ],
            'video': [
                {
                    'image': ''
                }
            ],
            'information': {
                'name': basic.nombres,
                'profesion': 'Ingeniero',
                'hobbies': 'cantar, bailar, tocar guitarra',
                'contextura': 'Delgada',
                'cabello': 'Negro, ondulado',
                'medidas': 'peso: 40kg, 1.70 mts'
            }
        };
        return  self.data;
    };
}]);
