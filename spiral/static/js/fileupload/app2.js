/*
 * jQuery File Upload Plugin Angular JS Example 1.2.1
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2013, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint nomen: true, regexp: true */
/*global window, angular */

var demo = angular.module('demo', ['blueimp.fileupload']);


demo.config(['$interpolateProvider', '$httpProvider', 'fileUploadProvider',function ($interpolateProvider, $httpProvider, fileUploadProvider) {

    delete $httpProvider.defaults.headers.common['X-Requested-With'];
    fileUploadProvider.defaults.redirect = window.location.href.replace(
        /\/[^\/]*$/,
        '/cors/result.html?%s'
    );
    var isOnGitHub = window.location.hostname === 'blueimp.github.io';
    if (isOnGitHub) {
        // Demo settings:
        angular.extend(fileUploadProvider.defaults, {
            // Enable image resizing, except for Android and Opera,
            // which actually support image resizing, but fail to
            // send Blob objects via XHR requests:
            disableImageResize: /Android(?!.*Chrome)|Opera/
                .test(window.navigator.userAgent),
            maxFileSize: 5000000,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i
        });
    }
}]);


var controllers = {};

controllers.DemoFileUploadController = function($scope,
                                                $http,
                                                $filter,
                                                $window){

    $scope.options = {
        url: '/upload/angular/'
    };

    var urlview = '/upload/view/',
        isOnGitHub = window.location.hostname === 'blueimp.github.io';

    if (!isOnGitHub) {
        $scope.loadingFiles = true;
        $http.get(urlview)
            .then(
            function (response) {
                $scope.loadingFiles = false;
                $scope.queue = response.data.files || [];
            },
            function () {
                $scope.loadingFiles = false;
            }
        );
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

demo.controller(controllers);