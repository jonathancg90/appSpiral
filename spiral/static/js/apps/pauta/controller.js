var controllers = {};

controllers.pautaController = function($scope, searchUrls, $http, $filter){
    var listPautaUrl = searchUrls.pautaListUrl,
        projectUrl = searchUrls.projectListUrl;

    var dateNow = new Date();
    $scope.editDate = false;
    $scope.pauta = {
        'date': $filter('date')(dateNow, 'dd/MM/yyyy')
    };
    debugger
    $http.get(listPautaUrl)
        .then(function(response) {
            debugger
            if(response.status == 200) {
                debugger
                $scope.pautas = response.data.pautas
            }else {
                $scope.pautas = [];
            }
        });

    $http.get(projectUrl)
        .then(function(response) {
            if(response.status == 200) {
                $scope.projects = response.data.project
            }else {
                $scope.projects = [];
            }
        });

};

pautaApp.controller(controllers);