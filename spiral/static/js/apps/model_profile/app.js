'use strict';
var modelApp = angular.module('modelApp', ['blueimp.fileupload']);

modelApp.config(['$interpolateProvider', '$httpProvider', 'fileUploadProvider',function ($interpolateProvider, $httpProvider, fileUploadProvider) {
    // So '{{ }}' not overlaps with django syntax template
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');

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

modelApp.run(function(DjangoConstants, $http) {
    $http.defaults.headers.post['X-CSRFToken'] = DjangoConstants.csrfToken;
});