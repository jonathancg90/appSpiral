var controllers = {};

controllers.projectController = function($scope,
                                         commercialFactory,
                                         clientFactory,
                                         entryFactory,
                                         brandFactory,
                                         projectService,
                                         factoryUrl){

    $scope.project_service = projectService;
    $scope.lineCasting = false;
    $scope.lineExtras = false;
    $scope.lineRepresentacion = false;
    $scope.lineFotos = false;

    //Urls
    var urlCommercial = factoryUrl.commercialUrl,
        urlBrand = factoryUrl.brandUrl,
        urlClient = factoryUrl.clientUrl,
        urlTypeClient = factoryUrl.urlTypeClient,
        urlEntry = factoryUrl.entryUrl;

    var rpCommercial = commercialFactory.all(urlCommercial);
    rpCommercial.then(function(data) {
        $scope.commercials = data.commercial;
    });

    var rpClient = clientFactory.all(urlClient);
    rpClient.then(function(data) {
        $scope.clients = data.client;
    });

    var rpEntry = entryFactory.all(urlEntry);
    rpEntry.then(function(data) {
        $scope.entries = data.entry;
    });

    var rpTypeClient = clientFactory.getTypeClients(urlTypeClient);
    rpTypeClient.then(function(data) {
        $scope.typeClients = data.types;
    });

    $scope.addCommercialDate = function(){
        if($scope.project_service.commercial != undefined){
            var date = {'date': ''};
            $scope.project_service.commercial.dates.push(date)
        }
    };

    $scope.addDeliveryDate = function(date){
        if(date != undefined || date != ''){
            var date = {'date': date};
            $scope.project_service.deliveries.push(date);
        }
    };

    $scope.changeEntry = function(entry){
        urlBrand = urlBrand.replace(':entry', entry.id);
        var rpBrand = brandFactory.finByEntry(urlBrand);
        rpBrand.then(function(data) {
            $scope.brands = data.brand;
            urlBrand = urlBrand.replace(entry.id, ':entry');
        });
    };

    $scope.$on('changeLine', function(event, args) {
        var line = args.value;
        cleanStatusLines();
        if(line == 'Casting')
            $scope.lineCasting = true;
        if(line == 'Extras')
            $scope.lineExtras = true;
        if(line == 'Representacion')
            $scope.lineRepresentacion = true;
        if(line == 'Fotos')
            $scope.lineFotos = true;
    });

    function cleanStatusLines(){
        $scope.lineCasting = false;
        $scope.lineExtras = false;
        $scope.lineRepresentacion = false;
        $scope.lineFotos = false;
    }

};

projectApp.controller(controllers);