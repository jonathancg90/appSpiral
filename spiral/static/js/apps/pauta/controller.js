var controllers = {};

controllers.pautaController = function($scope, searchUrls, $http, $filter){
    var listPautaUrl = searchUrls.pautaListUrl,
        projectUrl = searchUrls.projectListUrl;

    var dateNow = new Date();
    $scope.editDate = false;
    $scope.details = [];
    $scope.pauta = {
        'date': $filter('date')(dateNow, 'dd/MM/yyyy')
    };
    $http.get(listPautaUrl)
        .then(function(response) {
            if(response.status == 200) {
                $scope.pautas = response.data.pautas;
                $scope.detail = get_detail_project();
            }else {
                $scope.pautas = []
            };

        });

    $http.get(projectUrl)
        .then(function(response) {
            if(response.status == 200) {
                $scope.projects = response.data.project
            }else {
                $scope.projects = [];
            }
        });

    function get_detail_project(){
        debugger
        if ($scope.pauta.id == undefined){
            $.each( $scope.pautas,function(ind_pauta, value_pauta){
                $.each(value_pauta.detail,function(i_detail, value_detail){
                    $scope.details.push(value_detail)
                })

            });
        }
    }

};

pautaApp.controller(controllers);