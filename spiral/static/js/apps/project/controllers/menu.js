var controllers = {};

controllers.menuController = function($scope, $rootScope){
    $scope.lines = ['Casting', 'Extras', 'Representacion', 'Fotos'];

    $scope.changeLine = function(option){
        $scope.lineSelected = option;
        $rootScope.$broadcast('changeLine', { value: option });
    }
};


projectApp.controller(controllers);