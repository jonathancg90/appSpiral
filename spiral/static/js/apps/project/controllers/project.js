var controllers = {};

controllers.projectController = function($scope,
                                         commercialFactory,
                                         clientFactory,
                                         entryFactory,
                                         brandFactory,
                                         projectFactory,
                                         projectService,
                                         factoryUrl,
                                         contextData,
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
    $scope.detailLoader = true;

    //-----------------------------------------------

    $rootScope.$on("saveProject", function(event, data){
        var validate = validateRequire();
        if(validate.status){
            var data = {
                'project': dataProject(),
                'client': dataClient(),
                'commercial': $scope.project_service.commercial,
                'line': dataLine(),
                'models': $scope.project_service.detailModel,
                'payment': dataPayment(),
                'resources': $scope.project_service.detailStaff
            };
            var url = urlProjectSave;
            if($scope.project_service.project_id != undefined){
                url = urlProjectUpdate;
            }

            var rpSaveProject = projectFactory.save(url, data);
            rpSaveProject.then(function(data) {
                if(data.status == 'success'){
                    $scope.flashMessage = data.message + ' : '+ data.result.code;
                }
                $scope.project_service.project_code = data.result.code;
                $scope.project_service.project_id = data.result.id;
                $scope.flashType = data.status;
            });
        } else {
            $scope.flashMessage = 'Campos requeridos incompletos: '+ validate.msg;
            $scope.flashType = 'warning';
        }
    });

    $rootScope.$on("setMessage", function(event, data){
        $scope.flashMessage = data.message;
        $scope.flashType = data.type;
    });

    $scope.$on('changeLine', function(event, args) {
        var line = args.value;
        cleanStatusLines();
        $scope.project_service.line = line;
        $scope.line = true;
        if(line.name == 'casting'){
            getCharacterCasting();
            getTypeCasting();
            $scope.lineCasting = true;
        }
        if(line.name == 'extra'){
            getCharacterExtra();
            $scope.lineExtras = true;
        }
        if(line.name == 'Representacion'){
            getCharacterRepresentation();
            $scope.lineRepresentacion = true;
        }
        if(line.name == 'Foto'){
            getCharacterCasting();
            getTypeCastingPhotoCasting();
            $scope.lineFotos = true;
        }
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
        urlCurrency = factoryUrl.urlCurrency,
        urlRoles = factoryUrl.urlRoles,
        urlEmployee = factoryUrl.urlEmployee,
        urlCharacter = factoryUrl.urlCharacterCasting,
        urlCharacterExtra = factoryUrl.urlCharacterExtra,
        urlEventRepresentation = factoryUrl.urlEventsRepresentation,
        urlSearchModel = factoryUrl.urlSearchModel,
        urlCharacterRepresentation = factoryUrl.urlCharacterRepresentation,
        urlPhotoCastingType = factoryUrl.urlPhotoCastingType,
        urlProjectUpdate = factoryUrl.urlProjectUpdate,
        urlDataUpdateProject = factoryUrl.urlDataUpdateProject,
        urlProjectSave = factoryUrl.projectSaveUrl;


    //-----------------------------------------------
    //Update
    //-----------------------------------------------

    var codeUpdate = contextData.codeUpdate,
        idUpdate = contextData.idUpdate;
    debugger

    updateProject(idUpdate);

    function updateProject(idUpdate){
        debugger
        var url = urlDataUpdateProject.replace(':pk', idUpdate);
        var rpUpdateProject = projectFactory.searchUrl(url);
        rpUpdateProject.then(function(data) {
            debugger
        });
    }

    //-----------------------------------------------
    //Request Methods
    //-----------------------------------------------

    var rpCommercial = commercialFactory.all(urlCommercial);
    rpCommercial.then(function(data) {
        $scope.commercials = data.commercial;
        $scope.detailLoader = false;
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

    var rpCurrency = projectFactory.searchUrl(urlCurrency);
    rpCurrency.then(function(data) {
        $scope.coins = data.currency;
    });

    var rpRoles = projectFactory.searchUrl(urlRoles);
    rpRoles.then(function(data) {
        $scope.roles = data.roles;
    });

    var rpEmployee = projectFactory.searchUrl(urlEmployee);
    rpEmployee.then(function(data) {
        $scope.productors = data.productors;
        $scope.realizers = data.realized;
    });


    //-----------------------------------------------
    //Project
    //-----------------------------------------------

    // Cambia estado del modal de detalle de modelos
    $scope.setStatusSave = function(value) {
        $scope.saveDetail = value;
        if(value){
            $scope.castDetailModel = {};
            $scope.detailStaff = {};
        }
    };
    //Busqueda de modelos a travez de un input
    $scope.$watch('castDetailModel.model_name', function(newValue, oldValue){
        if(newValue != oldValue){
            var model = getModelById(newValue);
            $scope.castDetailModel.model_name = model.name;
            $scope.castDetailModel.model = model;
        }
    });

    //Validacion antes de agregar fechas de filmacion
    $scope.addCommercialDate = function(){
        if($scope.project_service.commercial != undefined){
            var date = {'date': ''};
            $scope.project_service.commercial.dates.push(date)
        } else {
            $scope.flashMessage = 'Elija un comercial antes de agregar fechas';
            $scope.flashType = 'warning';
        }
    };

    //Agregar fechas de ebtrega
    $scope.addDeliveryDate = function(date){
        if(date != undefined || date != ''){
            var date = {'date': date};
            $scope.project_service.deliveries.push(date);
        }
    };

    //Agregar condiciones de pago
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

    //Cambia rubro en la creacion de comercial
    $scope.changeEntry = function(entry){
        urlBrand = urlBrand.replace(':entry', entry.id);
        var rpBrand = brandFactory.finByEntry(urlBrand);
        rpBrand.then(function(data) {
            $scope.brands = data.brand;
            urlBrand = urlBrand.replace(entry.id, ':entry');
        });
    };

    //Elimina detalle de modelos
    $scope.deleteDetailModel = function(position){
        if ($scope.project_service.detailModel.length !== 0) {
            $scope.project_service.detailModel.splice(position, 1);
        }
    };

    //Elimina detalle de staff
    $scope.deleteDetailStaff = function(position){
        if ($scope.project_service.detailStaff.length !== 0) {
            $scope.project_service.detailStaff.splice(position, 1);
        }
    };

    //Agrega detalle de staff
    $scope.addDetailStaff = function(addDetailStaff){
        $scope.project_service.detailStaff.push(addDetailStaff);
        $scope.detailStaff = {}
    };

    //actualizar registrro de staff
    $scope.updateStaffDetail = function(detail){
        $scope.detailStaff = detail;
        $scope.setStatusSave(false);
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
        if(client == undefined){
            $scope.flashMessage = 'Ingrese los datos del cliente';
            $scope.flashType = 'warning';
            return;
        }
        if(client.name != undefined &&
            client.ruc != undefined &&
            client.type !=undefined) {

            var data = {
                'name': client.name,
                'ruc': client.ruc,
                'address': client.address,
                'type': client.type
            };
            var rpSaveClient = clientFactory.saveClient(urlSaveClient, data);

            rpSaveClient.then(function (data) {
                if (data.status == 'success') {
                    $scope.flashMessage = data.message;
                    $scope.flashType = data.status;
                    $('#modalClient').modal('hide');
                    $scope.newClient = {};
                    angular.forEach(data.result.type, function (type, key) {
                        insertClientType(type, data.result);
                    })
                } else {
                    $scope.flashMessage = data.message;
                    $scope.flashType = data.status;
                }
            });
        } else {
            $scope.flashMessage = 'No se ha creaco al cliente: Falta llenar campos para crear al cliente';
            $scope.flashType = 'warning';
        }
    };

    //-----------------------------------------------
    //Foto Casting
    //-----------------------------------------------

    function getTypeCastingPhotoCasting(){
        var rpTypePhotoCasting = projectFactory.searchUrl(urlPhotoCastingType);
        rpTypePhotoCasting.then(function(data) {
            $scope.types = data.types;
        });
    }
    //-----------------------------------------------
    //Representation
    //-----------------------------------------------

    var rpEventRepresentation = projectFactory.searchUrl(urlEventRepresentation);
    rpEventRepresentation.then(function(data) {
        $scope.events = data.events;
    });

    function getCharacterRepresentation(){
        var rpCharacterRepresentation = projectFactory.searchUrl(urlCharacterRepresentation);
        rpCharacterRepresentation.then(function(data) {
            $scope.characters = data.character;
        });
    }

    $scope.searchModel = function(search){
        var data = {
            'name':  search
        };
        var rpSearchModel = projectFactory.searchPost(urlSearchModel, data);
        rpSearchModel.then(function(data) {
            $scope.models = data.models;
        });
    };

    function getModelById(id){
        result = undefined;
        angular.forEach($scope.models, function(value, key) {
            if(id == value.id){
                result = value;
            }
        });
        return result;
    };


    //-----------------------------------------------
    //Extra
    //-----------------------------------------------

    function getCharacterExtra(){
        var rpCharacterExtra = projectFactory.searchUrl(urlCharacterExtra);
        rpCharacterExtra.then(function(data) {
            $scope.characters = data.character;
        });
    }

    //-----------------------------------------------
    //Casting
    //-----------------------------------------------
    function getCharacterCasting(){
        var rpCharacter = projectFactory.searchUrl(urlCharacter);
        rpCharacter.then(function(data) {
            $scope.characters = data.character;
        });
    }
    function getTypeCasting(){
        var rpTypeCasting = projectFactory.searchUrl(urlTypeCasting);
        rpTypeCasting.then(function(data) {
            $scope.typeCasting = data.type;
        });
    }

    $scope.addDetailModel = function(newDetail){
        var validate = validateRequireModel(newDetail);
        if(validate) {
            $scope.project_service.detailModel.push(newDetail);
            $scope.castDetailModel = {}
        }
    };

    $scope.updateCastingDetail = function(detail){
        $scope.castDetailModel = detail;
        $scope.setStatusSave(false);
    };


    $scope.changeEmployeeRole = function(role){
        if(role.name == "Editor") {
            $scope.employees = $scope.realizers;
        }
        if(role.name == "Director") {
            $scope.employees = $scope.realizers;
        }
        if(role.name == "Productor") {
            $scope.employees = $scope.productors;
        }
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

    //-----------------------------------------------
    //Validations
    //-----------------------------------------------

    function validateRequire(){
        var status = true,
            msg = '';
        if($scope.project_service == undefined){
            status = false;
        }
        if($scope.project_service.line == undefined){
            status = false;
            status = false; msg += ' Linea de servicio no seleccionada | ';
        }
        if($scope.project_service.commercial == undefined || $scope.project_service.commercial == {}){
            status = false; msg += ' Comercial | ';
        }
        if($scope.project_service.startProduction == undefined || $scope.project_service.startProduction == ''){
            status = false; msg += ' Inicio de produccion | ';
        }
        if($scope.project_service.finishProduction == undefined || $scope.project_service.finishProduction == ''){
            status = false; msg += ' Final de produccion | ';
        }
        return {
            'status': status,
            'msg': msg
        };
    }

    function validateRequireModel(newDetail) {
        //Generic
        if (newDetail.character == undefined || newDetail.character == {}) {
            $scope.flashMessage = 'Falta indicar el tipo de personaje';
            $scope.flashType = 'warning';
            return false
        }

        //Casting
        if ($scope.project_service.line.name == 'casting'){
            if (newDetail.cant == undefined || newDetail.cant == '') {
                $scope.flashMessage = 'Falta indicar la cantidad de modelos';
                $scope.flashType = 'warning';
                return  false;
            }
            if (newDetail.type == undefined || newDetail.type == {}) {
                $scope.flashMessage = 'Falta indicar el tipo de casting';
                $scope.flashType = 'warning';
                return false
            }
        }
        //Extras
        if($scope.project_service.line == 'extra'){
            if (newDetail.cant == undefined || newDetail.cant == '') {
                $scope.flashMessage = 'Falta indicar la cantidad de modelos';
                $scope.flashType = 'warning';
                return  false;
            }
        }
        //Representacion
        if($scope.project_service.line == 'Representacion'){

        }
        //Foto
        if($scope.project_service.line == 'Foto'){
            if (newDetail.cant == undefined || newDetail.cant == '') {
                $scope.flashMessage = 'Falta indicar la cantidad de modelos';
                $scope.flashType = 'warning';
                return  false;
            }
        }
        return true;
    }

    //-----------------------------------------------
    //Parse DATA
    //-----------------------------------------------

    function dataProject(){
        var currency = undefined;
        if($scope.project_service.payment.currency != undefined)
            currency = $scope.project_service.payment.currency.id;

        return {
            'line_productions': $scope.project_service.line.id,
            'commercial': $scope.project_service.commercial.id,
            'start_productions': $scope.project_service.startProduction,
            'end_productions': $scope.project_service.finishProduction,
            'currency': currency,
            'budget': $scope.project_service.budget,
            'budget_cost': $scope.project_service.internalBudget,
            'observations': $scope.project_service.observation
        }
    }

    function dataClient(){
        var agency = undefined,
            productor = undefined,
            director = undefined;

        if($scope.project_service.agency != undefined)
            agency = $scope.project_service.agency.id;
        if($scope.project_service.agency != undefined)
            productor = $scope.project_service.productor.id;
        if($scope.project_service.agency != undefined)
            director = $scope.project_service.director.id;

        return {
            'agency': agency,
            'productor': productor,
            'director': director
        };
    }

    function dataLine(){
        if($scope.project_service.line.name == 'casting'){
            return  {
                'ppi': $scope.project_service.ppi,
                'ppg': $scope.project_service.ppg,
                'type_casting': $scope.project_service.typeCasting
            }
        }
        if($scope.project_service.line == 'extras'){
            return  {}
        }
        if($scope.project_service.line == 'representacion'){
            return  {
                'photo_use': $scope.project_service.use_photo,
                'type_event': $scope.project_service.event.id
            }
        }
        if($scope.project_service.line == 'fotos'){
            return  {
                'photo_use': $scope.project_service.use_photo,
                'type_casting': $scope.project_service.type.id
            }
        }
    }

    function dataPayment(){
        var client = undefined;

        if($scope.project_service.payment.client != undefined)
            client = $scope.project_service.payment.client.id;
        return {
            'client': client,
            'conditions': $scope.project_service.conditions
        }
    }
};

projectApp.controller(controllers);