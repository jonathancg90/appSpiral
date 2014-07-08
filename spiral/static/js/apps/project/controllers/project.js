var controllers = {};

controllers.projectController = function($scope,
                                         commercialFactory,
                                         clientFactory,
                                         projectService,
                                         factoryUrl){
    $scope.project_service = projectService;

    //Urls
    var urlCommercial = factoryUrl.commercialUrl,
        urlBrand = factoryUrl.brandUrl,
        urlClient = factoryUrl.clientUrl,
        urlEntry = factoryUrl.entryUrl;

    var rpCommercial = commercialFactory.all(urlCommercial);
    rpCommercial.then(function(data) {
        $scope.commercials = data.commercial;
    });

    var rpClient = clientFactory.all(urlClient);
    rpClient.then(function(data) {
        $scope.clients = data.client;
    });

    $scope.items = [];
};

projectApp.controller(controllers);