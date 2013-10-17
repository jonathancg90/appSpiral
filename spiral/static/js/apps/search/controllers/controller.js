var controllers = {};

controllers.SearchBasicController = function($scope, ModelFactory){
    $scope.models = ModelFactory.getBasicData();
};

controllers.SearchAdvanceController = function($scope, ModelFactory){
    $scope.models = ModelFactory.getAdvanceData();
}

searchApp.controller(controllers);