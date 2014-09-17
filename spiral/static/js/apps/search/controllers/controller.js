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
    $scope.paginate = 0;
    $scope.tooltip = [];
    $scope.typeSearch = {
        'simple': true,
        'advance': false
    };
    $scope.cant_result = 0;
    angular.element('#advance').hide();

    $scope.$watch('search', function(newValue, oldValue) {
        if(newValue != oldValue) {
            if($scope.find != undefined) {
                if(newValue.length < $scope.find.length ) {
                    $scope.models = [];
                    $scope.find = undefined;
                    $scope.paginate = 0;
                }
            }
        }
    });

    $scope.getFeatures = function() {
        $http.get(features)
            .then(function(response) {
                if(response.status == 200) {
                    $scope.listTags = getTags(response.data);
                    $scope.occupations = response.data.occupations
                }else {
                    $scope.listTags = [];
                }
            });
    };

    $scope.loadTags = function(query) {
        return $filter("filter")($scope.listTags, query);
    };

    $scope.changeType = function(type) {
        $scope.models = [];
        $rootScope.countInitial = '';
        if(type == 'simple'){
            $scope.typeSearch.simple = true;
            $scope.typeSearch.advance = false;
        }
        if(type == 'advance'){
            $scope.typeSearch.simple = false;
            $scope.typeSearch.advance = true;
        }
        $scope.paginate = 0;
        $scope.cant_result = 0;
        $scope.search = "";
        if($scope.typeSearch.advance){
            angular.element('#simple').hide();
            angular.element('#advance').show();
        }
        else{
            angular.element('#advance').hide();
            angular.element('#simple').show();
        }
    };

    $scope.getOccupation = function(summary) {
        var value = '';
        if(summary != undefined){
            angular.forEach($scope.occupations, function(occupation, fkey) {
                if(summary.indexOf(''+occupation.id) > -1){
                    value = occupation.name;
                }
            });
            return value;
        }
        return 'Sin ocupacion';
    };

    $scope.searchModel = function(event) {
        if(event.keyCode == 13){
            if($scope.search != undefined) {
                var last = search();
                if(last)
                    $scope.paginate = -1;
            }
        }
    };

    $scope.searchModelPaginate = function(){
        if($scope.search != undefined && $scope.search.length > 0) {
            search();
        } else {
            if($scope.typeSearch.advance){
                var last = addPage();
                if(last)
                    $scope.paginate = -1;
            }
        }
    };

    function search(){
        if($scope.search.length == 0){
            $scope.flashType = 'warning';
            $scope.flashMessage = 'Ingrese algun parametro de busqueda';
            return;
        }

        var type = undefined;

        if($scope.typeSearch.simple)
            type = 1;

        $scope.mode = $scope.search.indexOf('"') != -1?true:false;
        if($scope.mode){
            var b = /"/g;
            $scope.search = $scope.search.replace(b,"");

        }
        if($scope.models != undefined){
            if ($scope.models.length == 0 && $scope.paginate == -1)
                $scope.paginate = 0;
        }
        var data = {
            'text': $scope.search,
            'type': type,
            'paginate': $scope.paginate,
            'mode': $scope.mode
        };
        if($scope.typeSearch.simple) {
            $scope.loader = true;
            var response = ModelFactory.Search(searchUrl, data);
            response.then(function(models) {
                if(models.length > 0){
                    $scope.find = $scope.search;
                    $scope.loader = false;
                    $rootScope.countInitial =  $scope.find;
                    $scope.cant_result = models.length;
                    if(models.length == 30){
                        $scope.paginate = $scope.paginate + 1;
                    } else {
                        $scope.paginate = -1;
                    }
                    if($scope.models == undefined){
                        $scope.models = models;
                    } else {
                        angular.forEach(models, function(model, fkey) {
                            $scope.models.push(model);
                        });
                    }
                } else {
                    $scope.flashType = 'warning';
                    $scope.flashMessage = 'No se ha encontrado resultados';
                    $scope.loader = false;
                }
            });
        }
    }

    $scope.searchAdvance =  function(){
        if($scope.typeSearch.advance &&  $scope.tags.length > 0){
            $scope.paginate = -1;
            $scope.loader = true;
            $scope.models = [];
            var data = {
                'text': '',
                'advance': angular.toJson(get_advance_params()),
                'type': 2,
                'mode': $scope.mode,
                'features': angular.toJson(get_feature_params())
            };
            var response = ModelFactory.Search(searchUrl, data);
            response.then(function(models) {
                $scope.all = models;
                $scope.cant_result = $scope.all.length;
                var last = addPage();
                if(last == false){
                    $scope.paginate = 1;
                }
                $scope.loader = false;
            });
        } else {
            $scope.flashType = 'warning';
            $scope.flashMessage = 'Revise los criterios ingresados';
        }
    };

    function addPage(){
       var more = 30,
           last = false,
           max = $scope.models.length + more;
        if(max > $scope.all.length){
            last = true;
            max = $scope.all.length;
        }
        for (var i=$scope.models.length;i<=max;i++) {
            $scope.models.push($scope.all[i]);
        }
        return last;
    }

    $scope.getDetail = function(model_id){
        var response = detailService.getDetail(detail, model_id);
        $scope.detailLoader = true;
        response.then(function(data){
            if(data.status != "warning"){
                $scope.detailLoader = false;
                $scope.detail =  data;
                $scope.detail.profile.facebook = '#';
                $scope.detail.profile.occupation = 'Sin ocupacion';
                angular.forEach($scope.detail.features, function(feature, fkey) {
                    if(feature.feature.indexOf("Ocupacion") > -1){
                        $scope.detail.profile.occupation = feature.value
                    }
                    if(feature.value.indexOf("Facebook") > -1){
                        $scope.detail.profile.facebook = feature.description
                    }
                });
            } else {
                $scope.flashType = data.status;
                $scope.flashMessage = data.message;
            }
        });
    };

    //Support functions
    //-----------------

    /*
    Return []
    Function for build tag help in
    the input advanced search, and set tooltip
     */
    function getTags(data){
        result = [];
        //Features
        angular.forEach(data.features, function(feature, fkey) {
            text = feature.feature_name;
            $scope.tooltip.push(
                {
                    name: text,
                    type: 'option'
                });
            angular.forEach(feature.feature_values, function(value, vkey) {
                result.push({
                    'id': value.value_id,
                    'text': text + ' ' + value.value_name,
                    'feature': true
                });
            });
        });
        //Nacionalidad
        $scope.tooltip.push(
            {
                name: "Nacionalidad",
                type: "option"
            });
        angular.forEach(data.nationalities, function(value, fkey) {
            result.push({
                'id': value.id,
                'text': 'nacionalidad ' + value.nationality,
                'feature': false,
                'camp': 'sp_model.nationality_id'
            });
        });
        //Genero
        $scope.tooltip.push(
            {
                name: "genero",
                type: "option"
            });
        angular.forEach(data.genders, function(value, fkey) {
            result.push({
                'id': value.id,
                'text': 'genero ' + value.text,
                'feature': false,
                'camp': 'sp_model.gender'
            });
        });

        $scope.tooltip.push(
            {
                name: "edad",
                type: "range"
            });
        $scope.tooltip.push(
            {
                name: "estatura",
                type: "range"
            });
        $scope.tooltip.push(
            {
                name: "orden casting",
                type: "orden"
            });
        $scope.tooltip.push(
            {
                name: "orden extra",
                type: "orden"
            });
        $scope.tooltip.push(
            {
                name: "orden visita",
                type: "orden"
            });
        $scope.tooltip.push(
            {
                name: "solo web",
                type: "exclude"
            });
        $scope.tooltip.push(
            {
                name: "solo casting",
                type: "exclude"
            });

        return result;
    }

    /*
        Return []
        parse data for post in advance search (not feature)
     */
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
                    data.push({
                        'id': edades,
                        'feature': false,
                        'camp': 'sp_model.birth'
                    });
                }
                if(tag.text.indexOf("estatura") > -1){
                    var values= tag.text.split("-"),
                        estaturas = [];
                    for(var i=0; i<values.length; i++){
                        if(isNaN(parseInt(values[i])) == false){
                            estaturas.push(values[i]);
                        }
                    }
                    data.push({
                        'id': estaturas,
                        'feature': false,
                        'camp': 'sp_model.height'
                    });
                }
                if(tag.text.split("-").length == 2){
                    var values= tag.text.split("-");
                    if(values[1] == "web") {
                        data.push({
                            'id': 3,
                            'feature': false,
                            'camp': 'sp_model.status'
                        });
                    }
                    if(values[1] > "extra") {
                        data.push({
                            'id': values[1],
                            'feature': false,
                            'camp': 'sp_model.last_visit'
                        });
                    }
                    if(values[1] > "casting") {
                        data.push({
                            'id': values[1],
                            'feature': false,
                            'camp': 'sp_model.last_visit'
                        });
                    }
                }
                if(tag.text.indexOf("orden") > -1) {
                    var values= tag.text.split("-");
                    data.push({
                        'id': values[1],
                        'feature': false,
                        'camp': 'orden'
                    });
                }
            }
        });
        return data;
    }

    /*
        Return []
        parse feature data for post in advance search
     */
    function get_feature_params(){
        result = [];
        angular.forEach($scope.tags, function(feature, fkey) {
            if(feature.feature) {
                result.push(feature);
            }
        });
        return result;
    }

};

searchApp.controller(controllers);