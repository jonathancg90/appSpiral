var controllers = {};

controllers.SearchBasicController = function($scope, ModelFactory, $rootScope, detailService){
    $scope.models = ModelFactory.getBasicData();
    $scope.getDetail = function(model){
        $('#detailModal').modal('toggle');
        $scope.detail = detailService.getDetail(model);
    };
    $scope.prueba = 'hola';
};

controllers.SearchAdvanceController = function($scope, ModelFactory, detailService){
    $scope.models = ModelFactory.getAdvanceData();

    $scope.getModelGroups = function(){
        $scope.modelGroups = [];
        var i = 0,
            group =[];
        angular.forEach($scope.models, function(value, key){
            group.push(value);
            i ++;
            if(i == 4) {
                $scope.modelGroups.push(group);
                i = 0;
                group = [];
            }
        });
        return  $scope.modelGroups;
    };
    $scope.getDetail = function(model){
        $('#detailModal').modal('toggle');
        $scope.detail = detailService.getDetail(model);
    }
}

searchApp.controller(controllers);