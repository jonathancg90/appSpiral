var controllers = {};

controllers.searchController = function($scope, ModelFactory, detailService, searchUrls, $rootScope){
    var basic = searchUrls.search;
    $scope.loader = false;
    $scope.find = undefined;
    $scope.mode = false;

    $scope.typeSearch = {
        'simple': true,
        'advance': false
    };

    $scope.changeType = function(){
        $scope.typeSearch.simple = !$scope.typeSearch.simple;
        $scope.typeSearch.advance = !$scope.typeSearch.advance;
    };

    $scope.changeMode = function(){
        $scope.mode = $('#id-button-borders').prop('checked');
    };

    $scope.$watch('search', function(newValue, oldValue){
        if(newValue != oldValue) {
            if($scope.find != undefined) {
                if(newValue.length < $scope.find.length ){
                    $scope.models = [];
                    $scope.find = undefined;
                }
            }
        }
    });

    $scope.searchModel = function(event){
        if(event.keyCode == 13){
            var type = undefined;

            if($scope.typeSearch.simple)
                type = 1;
            if($scope.typeSearch.simple)
                type = 2;

            var data = {
                'text': $scope.search,
                'type': type,
                'mode': $scope.mode
            };

            if($scope.typeSearch.simple) {
                $scope.loader = true;
                var response = ModelFactory.basicSearch(basic, data);
                response.then(function(models) {
                    $scope.find = $scope.search;
                    $scope.loader = false;
                    $scope.models = models;
                    $rootScope.countInitial =  $scope.find;
                    console.log($scope.models);
                });
            }

            if($scope.typeSearch.advance){
                $scope.models = ModelFactory.advanceSearch(advance, data);
            }
        }
    };

    $scope.getDetail = function(model){
        $('#detailModal').modal('toggle');
        $scope.detail = detailService.getDetail(model);
    }
};

searchApp.controller(controllers);