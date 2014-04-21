var controllers = {};

controllers.ProfileController = function($scope, ModelFactory, modelUrls, modelData, modelStorage){
    $scope.model = modelStorage;
    var urlSave = modelUrls.save_model,
        urlCountries = modelUrls.urlCountries,
        urlSearch = modelUrls.urlSearch;
    $scope.docTypes = jQuery.parseJSON(modelData.docTypes);

    $scope.saveProfile = function(){
        if(required()){
            ModelFactory.setModel($scope.model);
            var message = ModelFactory.saveProfileData(urlSave);
            console.log(message);
        } else {
            console.log('falta llenar campos')
        }
    };

    $scope.countries = ModelFactory.getCountries(urlCountries);

    $scope.getModel = function(){
        $scope.model.id = $scope.model.code;
        $scope.model = ModelFactory.searchModel(urlSearch.replace(':pk', $scope.model.id));
    };

    function required(){
        if( $scope.model.name != undefined &&
            $scope.model.last_name != undefined &&
            $scope.model.email != undefined &&
            $scope.model.num_doc != undefined &&
            $scope.model.nationality != undefined){
            return true
        }
        return false
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
    $scope.features = jQuery.parseJSON(modelData.features);

    $scope.save_model_feature = function(feature){
        $scope.model.id = $scope.model.code;
        if( $scope.model.id != undefined){
            var message = ModelFactory.saveProfileData(urlSave.replace(':pk', $scope.model.id), feature);
            console.log(message);
        } else {
            console.log("selecionar un modelo");
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