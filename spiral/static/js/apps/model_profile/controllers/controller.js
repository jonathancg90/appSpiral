var controllers = {};

controllers.ProfileController = function($scope, ModelFactory, modelUrls, modelData, modelStorage) {
    $scope.model = modelStorage.model;
    var urlSave = modelUrls.save_model,
        urlCountries = modelUrls.urlCountries,
        urlSearch = modelUrls.urlSearch;

    $scope.docTypes = jQuery.parseJSON(modelData.docTypes);
    $scope.genders = jQuery.parseJSON(modelData.genders);
    $scope.pk = modelData.pk;

    $scope.flashType = '';
    $scope.flashMessage = '';
    $scope.optionalInput = false;
    $scope.created = false;

    $scope.$watch('pk', function(newValue) {
        if (newValue) {
            $scope.model.profile = {};
            $scope.model.profile['code']  = newValue;
            $scope.getModel();
        }
    });

    ModelFactory.getCountries(urlCountries).then(function(counries) {
        $scope.countries = counries;
    });

    $scope.showOptional = function(){
        $scope.optionalInput = ! $scope.optionalInput;
    };

    $scope.saveProfile = function(){
        if(required()){
            ModelFactory.setProfile($scope.model.profile);
            var response = ModelFactory.saveProfileData(urlSave);
            response.then(function(data){
                if(data.status == 'success'){
                    $scope.model.profile.code= data.code;
                }
                $scope.flashType = data.status;
                $scope.flashMessage = data.message;
            })
        } else {
            $scope.flashType = 'warning';
            $scope.flashMessage = 'falta llenar campos';
        }
    };

    $scope.getModel = function() {
        $scope.model.profile.id = $scope.model.profile.code;
        ModelFactory.searchModel(urlSearch.replace(':pk', $scope.model.profile.id)).then(function(model) {
            if(model.status == 'success'){
                $scope.created = true;
                $scope.$emit("Remove_Message");
                $scope.model.profile = model.profile;
                modelStorage.model.profile = $scope.model.profile;
                modelStorage.model.images = model.images;
                modelStorage.model.commercial = model.commercial;
                modelStorage.model.feature = model.features;
                updateChoicesProfile();
                //updateFeature(model.features);
                $('#modelActive').html(model.profile.name_complete);
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
        if( $scope.model.profile.name_complete != undefined &&
            $scope.model.profile.email != undefined &&
            $scope.model.profile.num_doc != undefined &&
            $scope.model.profile.nationality != undefined){
            return true
        }
        return false
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
        });

        //Direccion - Ciudad
        angular.forEach($scope.countries, function(value, key) {
        });

        //Nacionalidad
        if($scope.model.profile.nationality != 'No ingresado') {
            angular.forEach($scope.countries, function(value, key) {
                if($scope.model.profile.nationality_id == value.id){
                    $scope.model.profile.nationality = value;
                }
            });
        }
    }

    function updateFeature(features){
        angular.forEach(features, function(value, key) {
            $scope.model.feature[value.feature_id] = value;
        });

    }
};

controllers.DemoFileUploadController = function($scope,
                                                $http,
                                                $filter,
                                                $window,
                                                modelStorage){

    $scope.model = modelStorage.model;
    $scope.size = 0;

    var url = '/panel/model/model-control/save-picture/';

    $scope.options = {
        url: url
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
            debugger
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