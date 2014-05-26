var controllers = {};

controllers.searchController = function($scope, ModelFactory,
                                        detailService, searchUrls,
                                        $rootScope, $http, $filter){
    var searchUrl = searchUrls.search,
        detail = searchUrls.detail,
        profile = searchUrls.profile,
        features = searchUrls.features;
    $scope.loader = false;
    $scope.find = undefined;
    $scope.mode = false;
    $scope.detail = {};
    $scope.urlCrud = profile;
    $scope.size = 0;
    $scope.tooltip = '';
    $scope.typeSearch = {
        'simple': true,
        'advance': false
    };

    $scope.getFeatures = function(){
        $http.get(features)
            .then(function(response) {
                if(response.status == 200) {
                    $scope.listTags = getTags(response.data);
                }else {
                    $scope.listTags = [];
                }
            });
    };

    $scope.loadTags = function(query){
        return $filter("filter")($scope.listTags, query);
    };

    $scope.changeType = function(){
        $scope.typeSearch.simple = !$scope.typeSearch.simple;
        $scope.typeSearch.advance = !$scope.typeSearch.advance;
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
            if($scope.search != undefined){
                var type = undefined;

                if($scope.typeSearch.simple)
                    type = 1;

                $scope.mode = $scope.search.indexOf('"') != -1?true:false;
                if($scope.mode){
                    var b = /"/g;
                    $scope.search = $scope.search.replace(b,"");
                }

                var data = {
                    'text': $scope.search,
                    'type': type,
                    'mode': $scope.mode
                };

                if($scope.typeSearch.simple) {
                    $scope.loader = true;
                    var response = ModelFactory.Search(searchUrl, data);
                    response.then(function(models) {
                        $scope.find = $scope.search;
                        $scope.loader = false;
                        $scope.models = models;
                        $rootScope.countInitial =  $scope.find;
                        console.log($scope.models);
                    });
                }
            }
        }
    };

    $scope.searchAdvance =  function(){
        if($scope.typeSearch.advance &&  $scope.tags.length > 0){
            $scope.loader = true;
            var data = {
                'text': '',
                'type': 2,
                'mode': $scope.mode,
                'features':  $scope.tags
            };

            var response = ModelFactory.Search(searchUrl, data);
            response.then(function(models) {

            });
        } else {
            $scope.flashType = 'warning';
            $scope.flashMessage = 'Revise los criterios ingresados';
        }
    };

    $scope.getDetail = function(model_id){
        var response = detailService.getDetail(detail, model_id);
        response.then(function(data){
            $scope.detail =  data;
        });
    };

    function getTags(data){
        //Documentos
        result = [];
        angular.forEach(data, function(feature, fkey) {
            text = feature.feature_name;
            $scope.tooltip = $scope.tooltip + ' "' + text+ '" ';
            angular.forEach(feature.feature_values, function(value, vkey) {
                result.push({
                    'id': value.value_id,
                    'text': text + ' ' + value.value_name,
                    'feature': text
                });
            });
        });
        return result;
    }
};

searchApp.controller(controllers);