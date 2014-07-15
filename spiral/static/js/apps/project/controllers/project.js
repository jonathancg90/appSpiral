var controllers = {};

controllers.projectController = function($scope,
                                         commercialFactory,
                                         clientFactory,
                                         entryFactory,
                                         brandFactory,
                                         projectFactory,
                                         projectService,
                                         factoryUrl,
                                         $rootScope){

    $scope.project_service = projectService;
    $scope.lineCasting = false;
    $scope.lineExtras = false;
    $scope.lineRepresentacion = false;
    $scope.lineFotos = false;
    $scope.line = false;
    $scope.castDetailModel = {};
    $scope.newCommercial = {};
    $scope.newCondition = '';
    $scope.saveDetail = true;
    $scope.clientsProductor = [];
    $scope.clientsAgency = [];
    $scope.clientsDirector = [];

    $scope.setStatusSave = function(value) {
        $scope.saveDetail = value;
    };

    //-----------------------------------------------

    $rootScope.$on("setMessage", function(event, data){
        $scope.flashMessage = data.message;
        $scope.flashType = data.type;
    });

    $scope.$on('changeLine', function(event, args) {
        var line = args.value;
        cleanStatusLines();
        $scope.line = true;
        if(line == 'Casting')
            $scope.lineCasting = true;
        if(line == 'Extras')
            $scope.lineExtras = true;
        if(line == 'Representacion')
            $scope.lineRepresentacion = true;
        if(line == 'Fotos')
            $scope.lineFotos = true;
    });

    //-----------------------------------------------
    //Urls
    //-----------------------------------------------
    var urlCommercial = factoryUrl.commercialUrl,
        urlSaveCommercial = factoryUrl.commercialSaveUrl,
        urlSaveClient = factoryUrl.clientSaveUrl,
        urlBrand = factoryUrl.brandUrl,
        urlClient = factoryUrl.clientUrl,
        urlTypeClient = factoryUrl.urlTypeClient,
        urlEntry = factoryUrl.entryUrl,
        urlTypeCasting = factoryUrl.typeCastingUrl,
        urlCharacter = factoryUrl.urlCharacterCasting;

    //-----------------------------------------------
    //Request Methods
    //-----------------------------------------------

    var rpCommercial = commercialFactory.all(urlCommercial);
    rpCommercial.then(function(data) {
        $scope.commercials = data.commercial;
    });

    var rpClient = clientFactory.all(urlClient);
    rpClient.then(function(data) {
        $scope.clients = data.client;
        angular.forEach(data.client, function(value, key) {
            angular.forEach(value.type, function(type, key) {
                insertClientType(type, value);
            });
        });
    });

    var rpEntry = entryFactory.all(urlEntry);
    rpEntry.then(function(data) {
        $scope.entries = data.entry;
    });

    var rpTypeClient = clientFactory.getTypeClients(urlTypeClient);
    rpTypeClient.then(function(data) {
        $scope.typeClients = data.types;
    });

    //-----------------------------------------------
    //Project
    //-----------------------------------------------

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

    $scope.addCondition =  function(condition) {
        if(condition != undefined && condition != '') {
            if ($scope.project_service.conditions.indexOf(condition) == -1) {
                $scope.project_service.conditions.push(condition);
                $scope.newCondition = '';
                angular.element('#inputCondition').val('');
            } else {
                $scope.flashMessage = 'Condicion de pago repetido';
                $scope.flashType = 'warning';
            }
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

    $scope.deleteDetailModel = function(position){
        if ($scope.project_service.detailModel.length !== 0) {
            $scope.project_service.detailModel.splice(position, 1);
        }
    };

    //-----------------------------------------------
    //Modals Create
    //-----------------------------------------------

    $scope.saveCommercial = function(commercial) {
        var data = {
            'name': commercial.name,
            'brand': commercial.brandSelected.id
        };
        var rpSaveCommercial = commercialFactory.saveCommercial(urlSaveCommercial, data);

        rpSaveCommercial.then(function(data) {
            if(data.status == 'success'){
                $scope.flashMessage = data.message;
                $scope.flashType = data.status;
                $('#modalCommercial').modal('hide');
                $scope.newCommercial = {};
                $scope.commercials.push(data.result)
            } else {
                $scope.flashMessage = data.message;
                $scope.flashType = data.status;
            }
        });
    };

    $scope.saveClient = function(client) {
        var data = {
            'name': client.name,
            'ruc': client.ruc,
            'address': client.address,
            'type': client.type
        };
        var rpSaveClient = clientFactory.saveClient(urlSaveClient, data);

        rpSaveClient.then(function(data) {
            if(data.status == 'success') {
                $scope.flashMessage = data.message;
                $scope.flashType = data.status;
                $('#modalClient').modal('hide');
                $scope.newClient = {};
                angular.forEach(data.result.type, function(type, key) {
                    insertClientType(type, data.result);
                })
            } else {
                $('#modalClient').modal('hide');
                $scope.flashMessage = data.message;
                $scope.flashType = data.status;
            }
        });

    };

    //-----------------------------------------------
    //Casting
    //-----------------------------------------------

    var rpCharacter = projectFactory.searchUrl(urlCharacter);
    rpCharacter.then(function(data) {
        $scope.characters = data.character;
    });

    var rpTypeCasting = projectFactory.searchUrl(urlTypeCasting);
    rpTypeCasting.then(function(data) {
        $scope.typeCasting = data.type;
    });

    $scope.addDetailModel = function(newDetail){
        $scope.project_service.detailModel.push(newDetail);
        $scope.castDetailModel = {}
    };

    $scope.updateCastingDetail = function(detail){
        $scope.castDetailModel = detail;
        $scope.setStatusSave(false);
    };

    //-----------------------------------------------
    //Functions
    //-----------------------------------------------

    function cleanStatusLines(){
        $scope.lineCasting = false;
        $scope.lineExtras = false;
        $scope.lineRepresentacion = false;
        $scope.lineFotos = false;
    }

    function insertClientType(type, value){
        if(type.name == "Productora"){
            $scope.clientsProductor.push(value);
        }
        if(type.name == "Realizadora"){
            $scope.clientsDirector.push(value);
        }
        if(type.name == "Agencia"){
            $scope.clientsAgency.push(value);
        }
    }
};

projectApp.controller(controllers);