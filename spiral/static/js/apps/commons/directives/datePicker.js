var datePicker = angular.module('datePicker', []);

datePicker.directive('datePicker', function() {
    return {
        require: 'ngModel',
        restrict: 'A',
        link: function (scope, elem, attrs, ngModel) {
            elem.datepicker({
                dateFormat: 'dd/mm/yy',
                onSelect: function (text) {
                    scope.$apply(function () {
                        ngModel.$setViewValue(text);
                    });
                }
            });
        }
    }
});