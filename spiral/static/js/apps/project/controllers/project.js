var controllers = {};

controllers.projectController = function($scope, projectService){
    $scope.project_service = projectService;
};

projectApp.controller(controllers);