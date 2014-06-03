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
        $scope.models = [];
        $rootScope.countInitial = '';
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

    function get_advance_params(){
        var data = [];
        angular.forEach($scope.tags, function(tag, key) {
            if(tag.feature == false || tag.feature == undefined){
                if(tag.camp == 'sp_model.nationality_id'){
                    data.push(tag);
                }
                if(tag.camp == 'sp_model.gender'){
                    data.push(tag);
                }
                if(tag.text.indexOf("edad") > -1){
                    var values= tag.text.split("-"),
                        edades = [];
                    for(var i=0; i<values.length; i++){
                        if(isNaN(parseInt(values[i])) == false){
                            edades.push(values[i]);
                        }
                    }
                    debugger
                    data.push({
                        'id': edades,
                        'feature': false,
                        'camp': 'sp_model.birth'
                    });
                }
            }
        });
        return data;
    }

    function get_feature_params(){
        result = [];
        angular.forEach($scope.tags, function(feature, fkey) {
            if(feature.feature) {
                result.push(feature);
            }
        });
        return result;
    }

    $scope.searchAdvance =  function(){
        if($scope.typeSearch.advance &&  $scope.tags.length > 0){
            $scope.loader = true;
            var data = {
                'text': '',
                'advance': angular.toJson(get_advance_params()),
                'type': 2,
                'mode': $scope.mode,
                'features': angular.toJson(get_feature_params())
            };
            var response = ModelFactory.Search(searchUrl, data);
            response.then(function(models) {
                $scope.models = models;
                $scope.loader = false;
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
        result = [];
        //Features
        angular.forEach(data.features, function(feature, fkey) {
            text = feature.feature_name;
            $scope.tooltip = $scope.tooltip + ' "' + text+ '" ';
            angular.forEach(feature.feature_values, function(value, vkey) {
                result.push({
                    'id': value.value_id,
                    'text': text + ' ' + value.value_name,
                    'feature': true
                });
            });
        });
        //Nacionalidad
        angular.forEach(data.nationalities, function(value, fkey) {
            result.push({
                'id': value.id,
                'text': 'nacionalidad ' + value.nationality,
                'feature': false,
                'camp': 'sp_model.nationality_id'
            });
        });
        //Genero
        angular.forEach(data.genders, function(value, fkey) {
            result.push({
                'id': value.id,
                'text': 'genero ' + value.text,
                'feature': false,
                'camp': 'sp_model.gender'
            });
        });


        return result;
    }
};

searchApp.controller(controllers);