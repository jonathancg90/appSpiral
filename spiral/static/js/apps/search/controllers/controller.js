var controllers = {};

controllers.searchController = function($scope, ModelFactory,
                                        detailService, searchUrls,
                                        $rootScope, $http, $filter){
    var searchUrl = searchUrls.search,
        detail = searchUrls.detail,
        profile = searchUrls.profile,
        urlList = searchUrls.list,
        projectUrl = searchUrls.projectListUrl,
        characterUrl = searchUrls.projectCharacterUrl,
        urlSaveList = searchUrls.saveList,
        urlSaveModelList = searchUrls.saveModelList,
        features = searchUrls.features,
        urlMessage = searchUrls.urlMessage,
        saveModelPautalUrl = searchUrls.saveModelPautalUrl,
        urlSendMessage = searchUrls.sendMessageUrl,
        quickUpdateUrl = searchUrls.quickUpdateUrl,
        listParticipate = searchUrls.list_participate;

    $scope.loader = false;
    $scope.messageLoader = false;
    $scope.find = undefined;
    $scope.mode = false;
    $scope.detail = {};
    $scope.newList = false;
    $scope.urlCrud = profile;
    $scope.size = 0;
    $scope.infoMessage = {};
    $scope.myList = [];
    $scope.paginate = 0;
    $scope.tooltip = [];
    $scope.showParticipate = false;
    $scope.view = {
        'list': false,
        'card':  true
    };
    $scope.typeSearch = {
        'simple': true,
        'advance': false
    };
    $scope.cant_result = 0;
    angular.element('#advance').hide();

    //List Project
    $http.get(projectUrl)
        .then(function(response) {
            if(response.status == 200) {
                $scope.projects = response.data.project
            }else {
                $scope.projects = [];
            }
        });

    $scope.getCharacter = function(){
        if($scope.newPauta.project != null){
            var url = characterUrl.replace(':pk', $scope.newPauta.project.id);
            $http.get(url)
                .then(function(response) {
                    if(response.status == 200) {
                        $scope.characters = response.data.details
                    }else {
                        $scope.characters = [];
                    }
                });
        } else {
            $scope.characters = [];
        }
    };

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

    $scope.getMessage = function(model){
        $scope.infoMessage.model = model;
        $('#modalMessage').modal('show');
        $('#myProfile').modal('hide');

        $http.get(urlMessage)
            .then(function(response) {
                if(response.status == 200) {
                    $scope.messages = response.data.message;
                }else {
                    $scope.listTags = [];
                }
            });
    };

    $scope.getModalPauta = function(model){
        $scope.addModelPauta = {
            "model_code": model.profile.code,
            "name_complete": model.profile.name_complete
        };

        $('#addPauta').modal('show');
        $('#myProfile').modal('hide');
    };

    $scope.quickUpdateModel = function(){
        if($scope.formUpdate.$valid){
            $http.post(quickUpdateUrl, angular.toJson($scope.updateModel))
                .then(function(response) {
                    if(response.status == 200) {
                        $scope.flashType = 'success';
                        $scope.flashMessage = 'Modelo Actualizado';
                        $('#updateModel').modal('hide');
                        $scope.messages = response.data.message;
                        $scope.messageLoader = false;
                        angular.forEach($scope.models, function(model, key) {
                            if($scope.updateModel.model_code == model.model_code){
                                model.name_complete = $scope.updateModel.name_complete;
                                model.phone_mobil = $scope.updateModel.phone_mobil;
                                model.phone_fixed = $scope.updateModel.phone_fixed;
                                model.height = $scope.updateModel.height;
                                model.weight = $scope.updateModel.weight;
                                model.email = $scope.updateModel.email;
                                model.address = $scope.updateModel.address;
                            }
                        });

                    }
                });
        }else {
            $scope.flashModalType = 'warning';
            $scope.flashModalMessage = 'Formulario invalido, verifique la informacion ingresada';
        }
    };

    $scope.getModalUpdate = function(model){
        $scope.updateModel= {
            "model_code": model.model_code,
            "name_complete": model.name_complete,
            "phone_mobil": model.phone_mobil,
            "phone_fixed": model.phone_fixed,
            "height": parseFloat(model.height),
            "weight": parseFloat(model.weight),
            "email": model.email,
            "address": model.address
        };

        $('.modal').modal('hide');
        $('#updateModel').modal('show');
    };


    $scope.saveModelPauta = function(){
        if($scope.newPauta.project != undefined &&
            $scope.newPauta.time != undefined &&
            $scope.newPauta.character != undefined){
            $scope.newPauta.model = $scope.addModelPauta;
            $http.post(saveModelPautalUrl, angular.toJson($scope.newPauta))
                .then(function(response) {
                    $scope.flashType = response.data.status;
                    $scope.flashMessage = response.data.message;

                    if(response.data.status == 'success') {
                        var dateNow = new Date();
                        $('#addPauta').modal('hide');
                        $scope.newPauta = {
                            'date': $filter('date')(dateNow, 'dd/MM/yyyy')
                        };
                    }
                });
        } else {
            $scope.flashModalType = 'warning';
            $scope.flashModalMessage = 'Campos requeridos incompletos';
        }
    };

    $scope.sendMessage = function(){
        $scope.messageLoader = true;
        $http.post(urlSendMessage, angular.toJson($scope.infoMessage))
            .then(function(response) {
                if(response.status == 200) {
                    $scope.flashType = 'success';
                    $scope.flashMessage = 'Mensaje enviado';
                    $('#modalMessage').modal('hide');
                    $('#myProfile').modal('show');
                    $scope.messages = response.data.message;
                    $scope.messageLoader = false;
                }else {
                    $scope.flashType = 'warning';
                    $scope.flashMessage = 'No se pudo enviar el mensaje al modelo';
                    $scope.messageLoade = false;
                }
            });
    };

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

    $scope.getList = function(model){
        $scope.list_participate = [];
        $scope.showParticipate = false;
        $scope.addModel = {
            'name': model.name_complete,
            'id': model.id
        };

        if($scope.myList.length == 0){
            $http.get(urlList)
                .then(function(response) {
                    if(response.status == 200) {
                        $scope.myList = response.data.list;
                    }else {
                        $scope.myList = [];
                    }
                });
        }
        var url = listParticipate.replace(":pk", model.id);
        $http.get(url, { cache: false}).then(function(response) {
            if(response.status == 200) {
                $scope.list_participate = response.data.list;

            }else {
                $scope.list_participate = [];
            }
        });

    };

    $scope.saveList = function(){
        if($scope.newTitleList != undefined || $scope.newTitleList != ''){
            var data = {
                'title': $scope.newTitleList
            };
            $http.post(urlSaveList, angular.toJson(data))
                .then(function(response) {
                    if(response.status == 200) {
                        $scope.myList.push(response.data.result);
                        $scope.newList = false;
                        $scope.newTitleList ='';
                    }else {
                        $scope.myList = [];
                    }
                });
        }
    };

    $scope.addModelList = function(){
        if($scope.listSelected != undefined || $scope.listSelected != ''){
            var data = {
                'model_id': $scope.addModel.id,
                'list_id': $scope.listSelected.id
            };

            $http.post(urlSaveModelList, angular.toJson(data))
                .then(function(response) {
                    if(response.status == 200) {
                        $scope.flashType = response.data.status;
                        $scope.flashMessage = response.data.message;
                    }else {
                        $scope.myList = [];
                    }
                });
        }
    };

    $scope.changeView = function(view){
        debugger
        if(view == 'list'){
            $scope.view.list = true;
            $scope.view.card = false;
        } else {
            $scope.view.list = false;
            $scope.view.card = true;
        }
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
            debugger
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
                name: "visita",
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
        debugger
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
                if(tag.text.indexOf("solo") > -1) {
                    if(tag.text.split("-").length == 2) {
                        var values = tag.text.split("-");
                        if (values[1] == "web") {
                            data.push({
                                'id': 3,
                                'feature': false,
                                'camp': 'sp_model.status'
                            });
                        }
                        if (values[1] == "extra") {
                            data.push({
                                'id': values[1],
                                'feature': false,
                                'camp': 'sp_model.last_visit'
                            });
                        }
                        if (values[1] == "casting") {
                            data.push({
                                'id': 'True',
                                'feature': false,
                                'camp': 'sp_model.last_visit'
                            });
                        }
                    }
                }
                if(tag.text.split('-')[0].indexOf("orden") > -1) {
                    var values= tag.text.split("-");
                    data.push({
                        'id': values[1],
                        'feature': false,
                        'camp': 'orden'
                    });
                }
                if(tag.text.split('-')[0].indexOf("visita") > -1) {
                    var values= tag.text.split("-"),
                        fechas = [];
                    for(var i=0; i<values.length; i++){
                        if(isNaN(parseInt(values[i])) == false){
                            fechas.push(values[i]);
                        }
                    }
                    data.push({
                        'id': fechas,
                        'feature': false,
                        'camp': 'sp_model.last_visit'
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