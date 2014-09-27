var controllers = {};

controllers.listController = function($scope, searchUrls, $http){
    var listModelUrl = searchUrls.listModelUrl,
        saveModellUrl = searchUrls.saveUrl,
        updateModellUrl = searchUrls.updateDetailUrl,
        urlDetail = searchUrls.detailUrl;

    $scope.newDetail = {};
    $scope.isSave = true;

    $http.get(listModelUrl)
        .then(function(response) {
            if(response.status == 200) {
                $scope.details = response.data.models
            }else {
                $scope.details = [];
            }
        });

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
        debugger
        $http.post(updateModellUrl, angular.toJson($scope.newDetail))
            .then(function(response) {
                debugger
                if(response.status == 200) {
                    $scope.newDetail = {};
                } else {
                    $scope.details = [];
                }
            });
    }

};

listApp.controller(controllers);