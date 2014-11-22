var controllers = {};

controllers.listController = function($scope, searchUrls, $http, $filter){
    var listModelUrl = searchUrls.listModelUrl,
        saveModellUrl = searchUrls.saveUrl,
        changeAvailableUrl = searchUrls.changeAvailable,
        projectUrl = searchUrls.projectListUrl,
        characterUrl = searchUrls.projectCharacterUrl,
        updateModellUrl = searchUrls.updateDetailUrl,
        saveModelPautalUrl = searchUrls.saveModelPautalUrl,
        urlDetail = searchUrls.detailUrl;
    var dateNow = new Date();

    $scope.newDetail = {};
    $scope.isSave = true;
    $scope.newPauta = {
        'date': $filter('date')(dateNow, 'dd/MM/yyyy')
    };

    //List Model
    $http.get(listModelUrl)
        .then(function(response) {
            if(response.status == 200) {
                $scope.details = response.data.models
            }else {
                $scope.details = [];
            }
        });

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

    $scope.addPauta = function(model){
        $scope.addModelPauta = model;
    };

    $scope.saveModelPauta = function(){
        if($scope.newPauta.project != undefined &&
            $scope.newPauta.time != undefined &&
            $scope.newPauta.character != undefined){
            $scope.newPauta.model = $scope.addModelPauta;
            $http.post(saveModelPautalUrl, angular.toJson($scope.newPauta))
                .then(function(response) {
                    $scope.flashModalType = response.data.status;
                    $scope.flashModalMessage = response.data.message;

                    if(response.data.status == 'success') {
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

    $scope.showSave = function(){
        $scope.isSave =true;
        $scope.newDetail = {};
    };

    $scope.showUpdate = function(detail){
        $scope.isSave=false;
        $scope.newDetail = detail;
    };

    $scope.getDetail = function(model_id){
        var response = $http.get(urlDetail.replace(':pk', model_id)).then(
            function(response) {
                if(response.status == 200) {
                    if(response.data.status == "success"){
                        $scope.detailLoader = false;
                        $scope.detail =  response.data;
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
                } else {

                }
        });

        $scope.detailLoader = true;

    };

    $scope.changeAvailable = function(detail){
        detail.available = !detail.available;
        $http.post(changeAvailableUrl, angular.toJson(detail))
            .then(function(response) {
                if(response.status == 200) {
                    $scope.flashType = response.data.status;
                    $scope.flashMessage = response.data.message;
                }
            });

    };

    $scope.saveDetail = function(){
        $http.post(saveModellUrl, angular.toJson($scope.newDetail))
            .then(function(response) {
                if(response.status == 200) {
                    $scope.newDetail = {};
                    $scope.details.push(response.data.model);
                } else {
                    $scope.details = [];
                }
            });

    };

    $scope.updateDetail = function(){
        $http.post(updateModellUrl, angular.toJson($scope.newDetail))
            .then(function(response) {
                if(response.status == 200) {
                    $scope.flashType = response.data.status;
                    $scope.flashMessage = response.data.message;
                    $scope.newDetail = {};
                } else {
                    $scope.details = [];
                }
            });
    }

};

listApp.controller(controllers);