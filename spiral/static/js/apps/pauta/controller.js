var controllers = {};

controllers.pautaController = function($scope, searchUrls, $http, $filter, contextData){
    var listPautaUrl = searchUrls.pautaListUrl,
        pautaStatusUpdateUrl = searchUrls.pautaStatusUpdateUrl,
        projectUrl = searchUrls.projectListUrl;

    var dateNow = new Date();
    $scope.editDate = false;
    $scope.details = [];
    $scope.pauta = {
        'date': $filter('date')(dateNow, 'dd/MM/yyyy')
    };
    $scope.status = jQuery.parseJSON(contextData.listStatus);

    $http.get(projectUrl)
        .then(function(response) {
            if(response.status == 200) {
                $scope.projects = response.data.project
            }else {
                $scope.projects = [];
            }
        });

    $scope.updateList = function(){
        var url = listPautaUrl;
        if($scope.pautas != undefined){
            if($scope.pautas.length > 0){
                var project_id = '';
                if($scope.pauta.project != undefined){
                    project_id = $scope.pauta.project.id
                }

                url = url + '?date=' +$scope.pauta.date +'&project='+project_id;
            }
        }
        $http.get(url)
            .then(function(response) {
                if(response.status == 200) {
                    $scope.pautas = [];
                    $scope.details = [];
                    $scope.pautas = response.data.pautas;
                    get_detail_project();
                }else {
                    $scope.pautas = []
                }

            });
    };


    $scope.updateStatusDetail = function(detail){
        var url = pautaStatusUpdateUrl,
            data = {
                'id':detail.id_detail,
                'status': detail.status.id
            };
        debugger
        $http.post(url, angular.toJson(data))
            .then(function(response) {
                if(response.status == 200) {
                    debugger
                    $scope.flashType = response.data.status;
                    $scope.flashMessage = response.data.message;
                }else {
                    $scope.pautas = []
                }

            });
    };

    $scope.changeDate = function(){
        $scope.editDate = !$scope.editDate;
        if($scope.editDate == false){
            $scope.updateList();
        }
    };

    function get_detail_project(){
        if ($scope.pauta.id == undefined){
            $scope.details = [];
            $.each( $scope.pautas,function(ind_pauta, value_pauta){
                $.each(value_pauta.detail,function(i_detail, value_detail){

                    $.each($scope.status,function(i_status, value_status){
                        if(value_detail.status == value_status.id){
                            value_detail.status=value_status;
                        }
                    });

                    $scope.details.push(value_detail)
                })

            });
        }
    }

    $scope.updateList();

};

pautaApp.controller(controllers);