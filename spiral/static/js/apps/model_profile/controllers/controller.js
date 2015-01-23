var controllers = {};

controllers.ProfileController = function($scope, ModelFactory, modelUrls, modelData, modelStorage) {
    $scope.model = modelStorage.model;
    var urlSave = modelUrls.save_model,
        urlUpdate = modelUrls.update_model,
        urlCountries = modelUrls.urlCountries,
        urlSearch = modelUrls.urlSearch,
        urlCommercial = modelUrls.urlCommercial;

    $scope.query_complete = 0;
    $scope.docTypes = jQuery.parseJSON(modelData.docTypes);
    $scope.genders = jQuery.parseJSON(modelData.genders);
    $scope.pk = modelData.pk;

    $scope.flashType = '';
    $scope.flashMessage = '';
    $scope.optionalInput = false;
    $scope.created = false;


    $scope.$watch('query_complete', function(newValue, oldValue){
        if(newValue == 1) {
            $scope.$watch('pk', function(newValue, oldValue){
                if(newValue){
                    debugger
                    if(modelData.pk != "" && modelData.pk != undefined){
                        $scope.model.profile = {};
                        $scope.model.profile['code']  = modelData.pk;
                        $scope.getModel();
                    }
                }
            });
        }
    });


    $scope.changeModel = function(){
        $scope.model = {};
        $('#commercial').html('');
        $scope.created = false;
    };

    ModelFactory.getCountries(urlCountries).then(function(counries) {
        $scope.countries = counries;
        $scope.query_complete += 1;
    });

    $scope.showOptional = function(){
        $scope.optionalInput = ! $scope.optionalInput;
        $scope.created = false
    };

    $scope.saveProfile = function(){
        var data_validate = required();
        if(data_validate.required){
            if($scope.model.profile.dir_country.cities.length == 0)
                $scope.model.profile.city = {city_id: undefined};

            ModelFactory.setProfile($scope.model.profile);
            if($scope.pk == undefined || $scope.pk == ""){
                url = urlSave;
            } else {
                url = urlUpdate.replace(':pk', $scope.pk);
            }

            var response = ModelFactory.saveProfileData(url);
            response.then(function(data){
                if(data.status == 'success'){

                    $scope.model.profile.code= data.code;
                    var url = urlCommercial.replace(':key', data.id);
                    $('#commercial').html('');
                    $('#commercial').html('<iframe src="'+url+'" scrolling="yes" height="100%" width="100% frameborder=0"></iframe>');
                }
                $scope.flashType = data.status;
                $scope.flashMessage = data.message;
            })
        } else {
            $scope.flashType = 'warning';
            $scope.flashMessage = 'falta llenar campos: ' + data_validate.msgValidate;
        }
    };

    $scope.getModel = function() {
        $scope.model.profile.id = $scope.model.profile.code;
        ModelFactory.searchModel(urlSearch.replace(':pk', $scope.model.profile.id)).then(function(model) {
            if(model.status == 'success'){
                $scope.pk = $scope.model.profile.code;
                $scope.created = true;
                $scope.$emit("Remove_Message");
                $scope.model.profile = model.profile;
                $scope.model.profile.height = parseFloat($scope.model.profile.height);
                $scope.model.profile.weight = parseFloat($scope.model.profile.weight);

                modelStorage.model.profile = $scope.model.profile;
                modelStorage.model.images = model.images;
                modelStorage.model.commercial = model.commercial;
                modelStorage.model.feature = model.features;
                updateChoicesProfile();
                //updateFeature(model.features);
                $('#modelActive').html(model.profile.name_complete);
                var url = urlCommercial.replace(':key', $scope.model.profile.id);
                $('#commercial').html('');
                $('#commercial').html('<iframe src="'+url+'" scrolling="yes" height="100%" width="100% frameborder=0"></iframe>'
                );
            } else {
                $scope.flashType = model.status;
                if(model.status == 'warning'){
                    $scope.model = {};
                    $scope.flashMessage = model.message;
                } else if(model.status == 'error'){
                    $scope.model = {};
                    $scope.flashMessage = model.message ;
                }
            }
        });
    };

    $scope.$on("Remove_Message", function(event){
        $scope.flashType = '';
        $scope.flashMessage = '';
    });

    function required(){
        var data = {};
        if($scope.model.profile == undefined){
            data = {
                msgValidate:'Todos',
                required: false
            };
            return data;
        }
        if( $scope.model.profile.name_complete == undefined){
            data = {
                msgValidate:'Nombre del modelo',
                required: false
            };
            return data;
        }
        if( $scope.model.profile.phone_mobil == undefined){
            data = {
                msgValidate:'Telefono',
                required: false
            };
            return data;
        }
        if( $scope.model.profile.birth == undefined){
            data = {
                msgValidate:'Fecha de Nacimiento',
                required: false
            };
            return data;
        }
        if($scope.model.profile.email == undefined){
            data = {
                msgValidate:'Email',
                required: false
            };
            return data;
        }
        if($scope.model.profile.num_doc == undefined){
            data = {
                msgValidate:'Documento de identidad',
                required: false
            };
            return data;
        }
        if($scope.model.profile.nationality == undefined){
            data = {
                msgValidate:'Nacionalidad',
                required: false
            };
            return data;
        }
        return { required: true};
    }

    function updateChoicesProfile(){

        //Año de nacimiento
        var array = [];
        array =  $scope.model.profile.birth.split("/");
        $scope.model.profile.birth = array[2]+'-'+array[1]+'-'+array[0];

        //Documentos
        angular.forEach($scope.docTypes, function(value, key) {
            if($scope.model.profile.type_doc == value.name) {
                $scope.model.profile.type_doc =  value;
            }
        });

        //Paises
        angular.forEach($scope.countries, function(value, key) {
            if($scope.model.profile.nationality == value.nationality){
                $scope.model.profile.nationality = value;
            }
        });

        //Genero
        angular.forEach($scope.genders, function(value, key) {
            if($scope.model.profile.gender == value.id){
                $scope.model.profile.gender = value;
            }
        });
        //Direccion - Pais
        angular.forEach($scope.countries, function(value, key) {
            if($scope.model.profile.country == value.id){
                $scope.model.profile.dir_country = value;
            }
        });

        //Direccion - Ciudad
        if($scope.model.profile.dir_country != undefined){
            angular.forEach($scope.model.profile.dir_country.cities, function(value, key) {
                if($scope.model.profile.city_id == value.city_id){
                    $scope.model.profile.city = value;
                }
            });
        }

        //Nacionalidad
        if($scope.model.profile.nationality != 'No ingresado') {
            angular.forEach($scope.countries, function(value, key) {
                if($scope.model.profile.nationality_id == value.id){
                    $scope.model.profile.nationality = value;
                }
            });
        }
    }

};

controllers.DemoFileUploadController = function($scope,
                                                $http,
                                                $filter,
                                                $window,
                                                modelUrls,
                                                modelStorage){

    $scope.model = modelStorage.model;
    $scope.size = 0;

    var url = '/panel/model/model-control/save-picture/';
    var urlDelete = modelUrls.urlDeletePicture;

    $scope.options = {
        url: url
    };
    $scope.deletePicture = function(id) {
        debugger
        urlDelete = urlDelete.replace(':pk', id);
        $http.get(urlDelete)
            .then(function(response) {
                debugger
            });
    };

};

controllers.AlbumController = function($scope, modelStorage){
    $scope.model = modelStorage.model;
};

controllers.FeatureController = function($scope, ModelFactory, modelUrls, modelData, modelStorage){
    var urlSave = modelUrls.save_feature,
        urlUpdate = modelUrls.update_feature,
        urlDelete = modelUrls.delete_feature;

    $scope.model = modelStorage.model;
    $scope.model.feature = {};
    $scope.features = jQuery.parseJSON(modelData.features);
    $scope.new_feature_description = [];

    $scope.get_feature =  function(feature_id){
        values = [];
        angular.forEach($scope.features, function(value, key) {
            if(value.feature_id == feature_id){
                values = value.feature_values;
            }
        });
        return values;
    };

    $scope.addFeature = function(feature, feature_value){
        valid = true;
        if(feature.type == "Valor Unico"){
            angular.forEach(modelStorage.model.feature, function(value, key) {
                if(value.feature_id == feature.feature_id){
                    valid = false;
                }
            });
        }
        if(valid){
            $scope.save_model_feature(feature_value);
        } else {
            $scope.flashType = 'warning';
            $scope.flashMessage = 'Esta carracteristica ya ha sido ingresado';
        }
    };

    $scope.save_model_feature = function(feature_value){
        if($scope.model.profile != undefined){
            var data = {
                'feature_value': feature_value
            };
            ModelFactory.saveFeatureData(urlSave.replace(':pk', $scope.model.profile.id), data).then(function(data) {
                if(data.status == 'success'){
                    modelStorage.model.feature.push(data.feature);
                } else {
                    $scope.flashType =data.status;
                    $scope.flashMessage = data.message;
                }
            });
        } else{
            $scope.flashType = 'warning';
            $scope.flashMessage = 'Antes debe de seleccionar un modelo';
        }
    };

    $scope.update_model_feature = function(model_feature_id, feature, description, index){
        if($scope.model.profile != undefined) {
            var data = {
                'model_feature_id': model_feature_id,
                'feature': feature,
                'description': description
            };
            ModelFactory.updateFeatureData(urlUpdate.replace(':pk', $scope.model.profile.id), data).then(function(data) {
                if(data.status == 'success') {
                    modelStorage.model.feature[index] = data.feature;
                } else {
                    $scope.flashType =data.status;
                    $scope.flashMessage = data.message;
                }
            });
        } else{
            $scope.flashType = 'warning';
            $scope.flashMessage = 'Antes debe de seleccionar un modelo';
        }
    };

    $scope.delete_model_feature = function(idx, model_feature_id){
        if($scope.model.profile != undefined){
            ModelFactory.deleteFeatureData(urlDelete, model_feature_id).then(function(data) {
                if(data.status == 'success'){
                    modelStorage.model.feature.splice(idx, 1);
                } else {
                    $scope.flashType =data.status;
                    $scope.flashMessage = data.message;
                }
            });
        } else{
            $scope.flashType = 'warning';
            $scope.flashMessage = 'Antes debe de seleccionar un modelo';
        }
    };
};

controllers.FileDestroyController = function($scope, $http){
    var file = $scope.file,
        state;
    if (file.url) {
        file.$state = function () {
            return state;
        };
        file.$destroy = function () {
            state = 'pending';
            return $http({
                url: file.deleteUrl,
                method: file.deleteType,
                xsrfHeaderName: 'X-CSRFToken',
                xsrfCookieName: 'csrftoken'
            }).then(
                function () {
                    state = 'resolved';
                    $scope.clear(file);
                },
                function () {
                    state = 'rejected';
                }
            );
        };
    } else if (!file.$cancel && !file._index) {
        file.$cancel = function () {
            $scope.clear(file);
        };
    }
};

modelApp.controller(controllers);