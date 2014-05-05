var controllers = {};

controllers.ProfileController = function($scope, ModelFactory, modelUrls, modelData, modelStorage) {
    $scope.model = modelStorage;
    var urlSave = modelUrls.save_model,
        urlCountries = modelUrls.urlCountries,
        urlSearch = modelUrls.urlSearch;
    $scope.docTypes = jQuery.parseJSON(modelData.docTypes);
    $scope.genders = jQuery.parseJSON(modelData.genders);

    $scope.flashType = '';
    $scope.flashMessage = '';
    $scope.optionalInput = false;
    $scope.created = false;

    $scope.showOptional = function(){
        $scope.optionalInput = ! $scope.optionalInput;
    };

    $scope.changeModel = function(){
        $scope.model = {};
        $scope.created = false;
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

    ModelFactory.getCountries(urlCountries).then(function(counries) {
        $scope.countries = counries;
    });

    $scope.getModel = function(){
        $scope.model.profile.id = $scope.model.profile.code;
        ModelFactory.searchModel(urlSearch.replace(':pk', $scope.model.profile.id)).then(function(model) {
            if(model.status == 'success'){
                $scope.created = true;
                $scope.$emit("Remove_Message");
                $scope.model.profile = model.profile;
                updateChoicesProfile();
                updateFeature(model.features);
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

        angular.forEach($scope.docTypes, function(value, key) {
            if($scope.model.profile.type_doc == value.name) {
                $scope.model.profile.type_doc =  value;
            }
        });

        angular.forEach($scope.countries, function(value, key) {
            if($scope.model.profile.nationality == value.nationality){
                $scope.model.profile.nationality = value;
            }
        });
    }

    function updateFeature(features){
        angular.forEach(features, function(value, key) {
            $scope.model.feature[value.id] = value.value;
        });

    }
};

controllers.DemoFileUploadController = function($scope,
                                                $http,
                                                $filter,
                                                $window){

    $scope.options = {
        url: '/panel/model/model-control/save-picture/'
    };

};


controllers.FeatureController = function($scope, ModelFactory, modelUrls, modelData, modelStorage){
    var urlSave = modelUrls.save_feature;

    $scope.model = modelStorage;
    $scope.model.feature = {};
    $scope.features = jQuery.parseJSON(modelData.features);

    $scope.$watch('features', function(newValue, oldValue) {
        if (newValue) {
            angular.forEach(newValue, function(value, key) {
                $scope.model.feature[value.feature_id] = '';
            });
        }
    });

    $scope.save_model_feature = function(feature){
        if($scope.model.profile != undefined){
            $scope.model.profile.id = $scope.model.profile.code;
            var response = ModelFactory.saveFeatureData(urlSave.replace(':pk', $scope.model.profile.id), feature);
            response.then(function(data) {
                if(data.status == 'success'){
                    debugger
                    $scope.model.feature[data.feature]= feature.value_name;
                } else {
                    $scope.flashType =data.status;
                    $scope.flashMessage = data.message;
                }
            });
        } else{
            $scope.flashType = 'warning';
            $scope.flashMessage = 'Antes debe de seleccionar un modelo';
        }
    }
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