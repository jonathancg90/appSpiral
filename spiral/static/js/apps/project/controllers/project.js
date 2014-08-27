var controllers = {};

controllers.projectController = function($scope,
                                         commercialFactory,
                                         clientFactory,
                                         entryFactory,
                                         brandFactory,
                                         projectFactory,
                                         typeContractFactory,
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
    $scope.newCondition = {};
    $scope.saveDetail = true;
    $scope.clientsProductor = [];
    $scope.clientsAgency = [];
    $scope.clientsDirector = [];
    $scope.detailLoader = true;
    $scope.loadDetail = false;

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
                'resources': $scope.project_service.detailStaff,
                'deliveries': $scope.project_service.deliveries,
                'duty': $scope.project_service.duty
            };
            var url = urlProjectSave;
            if($scope.project_service.id != undefined){
                url = urlProjectUpdate;
                data['project_id'] = $scope.project_service.id;
            }

            var rpSaveProject = projectFactory.save(url, data);
            rpSaveProject.then(function(data) {
                $('html, body').animate({
                        scrollTop: '0px'
                    },
                    1000);
                if(data.status == 'success'){
                    $scope.project_service.project_code = data.result.code;
                    $scope.project_service.id = data.result.id;
                    data.message = data.message + ' : '+ data.result.code;
                }
                $scope.flashMessage = data.message;
                $scope.flashType = data.status;

            });
        } else {
            $scope.flashMessage = 'Campos requeridos incompletos: '+ validate.msg;
            $scope.flashType = 'warning';
            msg_animate();
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
        urlUsePhoto = factoryUrl.urlUsePhoto,
        urlProjectUpdate = factoryUrl.urlProjectUpdate,
        urlCountryList = factoryUrl.urlCountryList,
        urlDataUpdateProject = factoryUrl.urlDataUpdateProject,
        urlTypeContract = factoryUrl.urlTypeContract,
        urlBroadcastList = factoryUrl.urlBroadcastList,
        urlSaveTypeContract = factoryUrl.urlSaveTypeContract,
        urlProjectSave = factoryUrl.projectSaveUrl;

    //-----------------------------------------------
    //Request Methods
    //-----------------------------------------------

    function getDataDuty(){
        var rpTypeContract = commercialFactory.all(urlTypeContract);
        rpTypeContract.then(function(data) {
            $scope.type_contract = data.type_contracts;
        });

        var rpBroadcast = commercialFactory.all(urlBroadcastList);
        rpBroadcast.then(function(data) {
            $scope.broadcasts = data.broadcasts;
        });


        var rpCountry = commercialFactory.all(urlCountryList);
        rpCountry.then(function(data) {
            $scope.countries = data.countries;
            $scope.detailLoader = false;
        });
    }

    var rpCommercial = commercialFactory.all(urlCommercial);
    rpCommercial.then(function(data) {
        $scope.commercials = data.commercial;
        getDataDuty();
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
    rpCurrency.success(function(data) {
        $scope.coins = data.currency;
    });

    var rpRoles = projectFactory.searchUrl(urlRoles);
    rpRoles.success(function(data) {
        $scope.roles = data.roles;
    });

    var rpEmployee = projectFactory.searchUrl(urlEmployee);
    rpEmployee.success(function(data) {
        $scope.productors = data.productors;
        $scope.realizers = data.realized;
    });

    /*-----------------------------------------
     | Update                                 |
     -----------------------------------------*/

    $scope.$watch('detailLoader', function(newValue, oldValue){
        if(newValue != oldValue){
            var codeUpdate = contextData.codeUpdate,
                idUpdate = contextData.idUpdate;
            var create = false;

            if($scope.pk == undefined){
                create = true;
            }
            $rootScope.$broadcast('setPermissions', {
                'permissions':jQuery.parseJSON(contextData.permissions) ,
                'create': create
            });
            if(newValue == false)
                updateProject(idUpdate, codeUpdate);
        }
    });

    function updateProject(idUpdate, codeUpdate){
        if(idUpdate == 0)
            return;
        var url = urlDataUpdateProject.replace(':pk', idUpdate);
        var rpUpdateProject = projectFactory.searchUrl(url);
        rpUpdateProject.success(function(data) {
            $rootScope.$broadcast('updateLine', {'line':data.result.line});

            data.result.codeUpdate = codeUpdate;
            projectService.set_result(data.result);
            $scope.project_service = projectService;
            $scope.$watch('loadDetail', function(newValue, oldValue){
                if(newValue){
                    processUpdate(data.result);
                }
            });
        });
        rpUpdateProject.error(function() {
            $scope.flashMessage = "Ha ocurrido un error, No se puede actualizar el proyecto";
            $scope.flashType ="error";
            msg_animate();
            $scope.detailLoader = true;
        });


    }

    function processUpdate(result){
        $scope.project_service = projectService;

        angular.forEach($scope.commercials, function(value, key) {
            if($scope.project_service.commercial.id == value.id) {
                $scope.project_service.commercial =  value;
            }
        });
        angular.forEach($scope.clientsProductor, function(value, key) {
            if(result.productor.id == value.id) {
                $scope.project_service.productor =  value;
            }
        });
        angular.forEach($scope.clientsAgency, function(value, key) {
            if(result.agency.id == value.id) {
                $scope.project_service.agency =  value;
            }
        });
        angular.forEach($scope.clientsDirector, function(value, key) {
            if(result.director.id == value.id) {
                $scope.project_service.director =  value;
            }
        });
        angular.forEach($scope.typeCasting, function(value_list, key_list) {
            angular.forEach(result.typeCasting, function(value, key) {
                if(value.id == value_list.id) {
                    $scope.project_service.typeCasting.push(value_list);
                }
            });
        });
        //Detail Staff
        angular.forEach($scope.project_service.detailStaff, function(value, key) {
            angular.forEach($scope.realizers, function(value_realizer, key_realizer) {
                if(value.employee.id_emp == value_realizer.id_emp) {
                    $scope.project_service.detailStaff[key].employee.last_name = value_realizer.last_name;
                    $scope.project_service.detailStaff[key].employee.name = value_realizer.name;
                }
            });
            angular.forEach($scope.productors, function(value_productor, key_productor) {
                if(value.employee.id_emp == value_productor.id_emp) {
                    $scope.project_service.detailStaff[key].employee.last_name = value_productor.last_name;
                    $scope.project_service.detailStaff[key].employee.name = value_productor.name;
                }
            });
        });
        //Detail Model
        angular.forEach($scope.project_service.detailModel, function(value, key) {
            if(value.currency != undefined) {
                angular.forEach($scope.coins, function(value_coins, key_coins) {
                    if(value.currency.id == value_coins.id) {
                        $scope.project_service.detailModel[key].currency = value_coins;
                    }
                });
            }
        });
        angular.forEach($scope.types, function(value, key) {
            if($scope.project_service.type.id == value.id) {
                $scope.project_service.type =  value;
            }
        });
        angular.forEach($scope.photoUses, function(value_list, key_list) {
            angular.forEach(result.use, function(value, key) {
                if(value.id == value_list.id) {
                    $scope.project_service.use.push(value_list);
                }
            });
        });
        if(result.payment.client != undefined){
            angular.forEach($scope.clients, function(value, key) {
                if(result.payment.client.id == value.id) {
                    $scope.project_service.payment.client =  value;
                }
            });
        }
        if(result.payment.currency != undefined){
            angular.forEach($scope.coins, function(value, key) {
                if(result.payment.currency.id == value.id) {
                    $scope.project_service.payment.currency =  value;
                }
            });
        }
        if(result.payment.currency != undefined){
            angular.forEach($scope.coins, function(value, key) {
                if(result.payment.currency.id == value.id) {
                    $scope.project_service.payment.currency =  value;
                }
            });
        }
        if(result.event != undefined){
            angular.forEach($scope.events, function(value, key) {
                if(result.event.id == value.id) {
                    $scope.project_service.event =  value;
                }
            });
        }

        //Duty
        if(result.duty != undefined) {
            angular.forEach($scope.countries, function(value_country, key) {
                angular.forEach(result.duty.countries, function(value, key) {
                    if(value.id == value_country.id) {
                        $scope.project_service.duty.countries.push(value_country);
                    }
                });
            });
            angular.forEach($scope.broadcasts, function(value_broadcast, key) {
                angular.forEach(result.duty.broadcasts, function(value, key) {
                    if(value.id == value_broadcast.id) {
                        $scope.project_service.duty.broadcasts.push(value_broadcast);
                    }
                });
            });
            angular.forEach($scope.type_contract, function(value, key) {
                if(result.duty.type_contract != undefined){
                    if(result.duty.type_contract.id == value.id) {
                        $scope.project_service.duty.type_contract =  value;
                    }
                }
            });
        }
    }

    /*---------------------------------------
    | Project                               |
    -----------------------------------------*/

    // Cambia estado del modal de detalle de modelos
    $scope.setStatusSave = function(value) {
        $scope.saveDetail = value;
        if(value){
            $scope.castDetailModel = {};
            $scope.detailStaff = {};
        }
    };
    //Busqueda de modelos a travez de un input
    $scope.$watch('castDetailModel.model_name', function(newValue, oldValue) {
        if(newValue != oldValue) {
            var model = getModelById(newValue);
            if(model != undefined){
                $scope.castDetailModel.model_name = model.name;
                $scope.castDetailModel.model = model;
            }
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
            msg_animate();
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
                var cond = {'name': condition};
                $scope.project_service.conditions.push(cond);
                $scope.newCondition.name = '';

            } else {
                $scope.flashMessage = 'Condicion de pago repetido';
                $scope.flashType = 'warning';
                msg_animate();
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
        if(addDetailStaff.percentage !=undefined &&
            addDetailStaff.budget !=undefined &&
            addDetailStaff.employee !=undefined){
            addDetailStaff.total = addDetailStaff.percent * addDetailStaff.budget;
            $scope.project_service.detailStaff.push(addDetailStaff);
            $scope.detailStaff = {}
            $('#modalStaffDetail').modal('hide');
        } else {
            $scope.flashMessage = 'Campos imcompletos';
            $scope.flashType = 'warning';
            msg_animate();
        }
    };

    //actualizar registrro de staff
    $scope.updateStaffDetail = function(detail) {
        $scope.detailStaff = detail;
        $scope.setStatusSave(false);

        if($scope.detailStaff.role != undefined) {
            angular.forEach($scope.roles, function(value, key) {
                if($scope.detailStaff.role.id == value.id) {
                    $scope.detailStaff.role =  value;
                    $scope.changeEmployeeRole($scope.detailStaff.role);
                }
            });
        }
        if($scope.detailStaff.employee != undefined){
            angular.forEach($scope.employees, function(value, key) {
                if($scope.detailStaff.employee.id == value.id) {
                    $scope.detailStaff.employee =  value;
                }
            });
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


    $scope.saveTypeContract = function(type_contract){
        if(type_contract == undefined){
            $scope.flashMessage = 'Ingrese los datos del tipo de contrato';
            $scope.flashType = 'warning';
            return;
        }
        var data = {
            'name': type_contract.name
        };
        var rpSaveTypeContract = typeContractFactory.save(urlSaveTypeContract, data);

        rpSaveTypeContract.then(function (data) {
            if (data.status == 'success') {
                $scope.flashMessage = data.message;
                $scope.flashType = data.status;
                $('#modalContract').modal('hide');
                $scope.type_contract.push(data.result.type);
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
            msg_animate();
        }
    };

    //-----------------------------------------------
    //Foto Casting
    //-----------------------------------------------

    function getTypeCastingPhotoCasting(){
        var rpTypePhotoCasting = projectFactory.searchUrl(urlPhotoCastingType);
        rpTypePhotoCasting.success(function(data) {
            $scope.types = data.types;
            getUsePhotoCasting();
        });
    }

    function getUsePhotoCasting(){
        var rpUsePhotos= projectFactory.searchUrl(urlUsePhoto);
        rpUsePhotos.success(function(data) {
            $scope.photoUses = data.uses;
            $scope.loadDetail = true;
        });
    }

    //-----------------------------------------------
    //Representation
    //-----------------------------------------------

    var rpEventRepresentation = projectFactory.searchUrl(urlEventRepresentation);
    rpEventRepresentation.success(function(data) {
        $scope.events = data.events;
    });

    function getCharacterRepresentation(){
        var rpCharacterRepresentation = projectFactory.searchUrl(urlCharacterRepresentation);
        rpCharacterRepresentation.success(function(data) {
            $scope.characters = data.character;
            $scope.loadDetail = true;
        });
    }

    $scope.searchModel = function(search){
        var data = {
            'name':  search
        };
        var rpSearchModel = projectFactory.searchPost(urlSearchModel, data);
        rpSearchModel.then(function(data) {
            if(data.status == 'success'){
                $scope.models = data.models;
            } else {
                $scope.flashMessage = data.message;
                $scope.flashType = data.status;
            }
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
    }

    //-----------------------------------------------
    //Extra
    //-----------------------------------------------

    function getCharacterExtra(){
        var rpCharacterExtra = projectFactory.searchUrl(urlCharacterExtra);
        rpCharacterExtra.success(function(data) {
            $scope.characters = data.character;
            $scope.loadDetail = true;
        });
    }

    //-----------------------------------------------
    //Casting
    //-----------------------------------------------
    function getCharacterCasting(){
        var rpCharacter = projectFactory.searchUrl(urlCharacter);
        rpCharacter.success(function(data) {
            $scope.characters = data.character;
        });
    }

    function getTypeCasting(){
        var rpTypeCasting = projectFactory.searchUrl(urlTypeCasting);
        rpTypeCasting.success(function(data) {
            $scope.typeCasting = data.type;
            $scope.loadDetail = true;
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

        if($scope.castDetailModel.character != undefined){
            angular.forEach($scope.characters, function(value, key) {
                if($scope.castDetailModel.character.id == value.id) {
                    $scope.castDetailModel.character =  value;
                }
            });
        }
        if($scope.castDetailModel.type != undefined){
            var data = [];
            angular.forEach($scope.typeCasting, function(value_list, key_list) {
                angular.forEach($scope.castDetailModel.type, function(value, key) {
                    if(value.id == value_list.id) {
                        data.push(value_list);
                    }
                });
            });
            $scope.castDetailModel.type = [];
            angular.forEach(data, function(value, key) {
                $scope.castDetailModel.type.push(value);
            })
        }
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
            if (newDetail.profile == undefined || newDetail.profile == {}) {
                $scope.flashMessage = 'Falta indicar el perfil del modelo';
                $scope.flashType = 'warning';
                return false
            }
        }
        //Extras
        if($scope.project_service.line.name == 'extra'){
            if (newDetail.cant == undefined || newDetail.cant == '') {
                $scope.flashMessage = 'Falta indicar la cantidad de modelos';
                $scope.flashType = 'warning';
                return  false;
            }
        }
        //Representacion
        if($scope.project_service.line.name == 'Representacion'){
            if (newDetail.model == undefined || newDetail.cant == '') {
                $scope.flashMessage = 'Falta indicar al modelo';
                $scope.flashType = 'warning';
                return  false;
            }
        }
        //Foto
        if($scope.project_service.line.name == 'Foto'){
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
        if($scope.project_service.productor != undefined)
            productor = $scope.project_service.productor.id;
        if($scope.project_service.director != undefined)
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
                'realized': $scope.project_service.realized,
                'type_casting': $scope.project_service.typeCasting
            }
        }
        if($scope.project_service.line.name == 'extra'){
            return  {}
        }
        if($scope.project_service.line.name == 'Representacion'){
            var event_id = undefined;
            if($scope.project_service.event != undefined){
                event_id = $scope.project_service.event.id
            }
            return {
                'type_event': event_id,
                'ppi': $scope.project_service.ppi,
                'ppg': $scope.project_service.ppg
            }
        }
        if($scope.project_service.line.name == 'Foto'){
            return  {
                'realized': $scope.project_service.realized,
                'uses': $scope.project_service.use,
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

    function msg_animate(){
        $('html, body').animate({
                scrollTop: '0px'
            },
            1000);
    }
};

projectApp.controller(controllers);