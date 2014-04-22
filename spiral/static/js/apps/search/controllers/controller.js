var controllers = {};

controllers.searchController = function($scope, ModelFactory, detailService, searchUrls){
    var basic = searchUrls.basic,
        advance = searchUrls.advance;


    $scope.typeSearch = {
        'simple': true,
        'advance': false
    };

    $scope.changeType = function(){
        $scope.typeSearch.simple = !$scope.typeSearch.simple;
        $scope.typeSearch.advance = !$scope.typeSearch.advance;
    };

    $scope.searchModel = function(event){
        if(event.keyCode == 13){

            var data = {
                'text': $scope.model
            };

            if($scope.typeSearch.simple){
                $scope.models = ModelFactory.basicSearch(basic, data);
            }

            if($scope.typeSearch.advance){
                $scope.models = ModelFactory.advanceSearch(advance, data);
            }
        }
    };

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
};

searchApp.controller(controllers);