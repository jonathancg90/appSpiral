var msgApp = angular.module('msgApp', []);

msgApp.directive('messageFlash', function () {
    return {
        restrict: 'E',
        scope: {
            message: '@',
            type: '@'
        },
        replace: true,
        template: "<div>\n    <div class=\'alert alert-block alert-success\' ng-show=\'success\'>\n        <button type=\'button\' class=\'close\'  ng-click=\"remove($event)\">\n            <i class=\'icon-remove\'></i>\n        </button>\n        <i class=\'icon-ok green\' ng-show=\'success\'></i>\n            {[{ message }]}\n    </div>\n\n    <div class=\'alert alert-block alert-warning\' ng-show=\'warning\'>\n        <button type=\'button\' class=\'close\'  ng-click=\"remove($event)\">\n            <i class=\'icon-remove\'></i>\n        </button>\n            <i class=\'icon-bullhorn yellow\' ng-show=\'warning\'></i>\n            {[{ message }]}\n    </div>\n\n    <div class=\'alert alert-block alert-error\' ng-show=\'error\'>\n        <button type=\'button\' class=\'close\' ng-click=\"remove($event)\">\n            <i class=\'icon-remove\'></i>\n        </button>\n            <i class=\'icon-ban-circle red\' ng-show=\'error\'></i>\n            {[{ message }]}\n    </div>\n</div>",
        link: function (scope, elem, attrs) {
            scope.$watch('type', function(type) {
                if (type) {
                    if (scope.type == 'success') {
                        scope.success = true;
                        scope.warning = false;
                        scope.error = false;
                    }
                    else if (scope.type == 'warning') {
                        scope.warning = true;
                        scope.error = false;
                        scope.success = false;
                    }
                    else if (scope.type == 'error') {
                        scope.error = true;
                        scope.success = false;
                        scope.warning = false;
                    }
                    else {
                        scope.error = false;
                        scope.success = false;
                        scope.warning = false;
                    }
                }
                scope.remove = function(e){
                    e.preventDefault();
                    scope.error = false;
                    scope.success = false;
                    scope.warning = false;
                    scope.$emit("Remove_Message");
                };
            });
        }
    };
});
