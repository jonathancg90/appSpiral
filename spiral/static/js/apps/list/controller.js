var controllers = {};

controllers.listController = function($scope, searchUrls, $http){
    var listModelUrl = searchUrls.listModelUrl;

    $http.get(listModelUrl)
        .then(function(response) {
            if(response.status == 200) {
                $scope.details = response.data.models
            }else {
                $scope.details = [];
            }
        });

};

listApp.controller(controllers);