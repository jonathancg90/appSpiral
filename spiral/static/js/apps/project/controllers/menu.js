var controllers = {};

controllers.menuController = function($scope,
                                      factoryUrl,
                                      projectService,
                                      $rootScope,
                                      projectFactory){

    var urlLine = factoryUrl.projectLineUrl;

    var rpLine = projectFactory.searchUrl(urlLine);
    rpLine.success(function(data) {
        $scope.lines  = data.lines;
    });

    $scope.projectService = projectService;

    $scope.$watch('projectService.commercial', function(newValue) {
        if (newValue) {
            $scope.commercial = ' >> '+newValue.name;
        }
    });

    $scope.$watch('projectService.project_code', function(newValue) {
        if (newValue) {
            $scope.project_code = ' >> '+newValue;
        }
    });

    $scope.changeLine = function(option){
        if($scope.lineSelected != undefined){
            projectService.clean(option);
        }
        $scope.lineSelected = ' >> ' + option.name;
        $scope.project_code = '';

        $rootScope.$broadcast('changeLine', { value: option });
        $rootScope.$broadcast('setLine', { });
    };
    $scope.$on('updateLine', function(event, args) {
         var line = args.line;
         $scope.changeLine(line);
    });
};


projectApp.controller(controllers);