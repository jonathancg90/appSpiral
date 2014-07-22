var chosen = angular.module('chosen', []);

chosen.directive('chosen', function() {
    return {
        restrict: 'A',
        link: function (scope, elem, attrs) {
            var list = attrs['list'];
            scope.$watch('list', function (newValue) {
                elem.trigger('liszt:updated');
                if(newValue){
                }
            });
            scope.$watch(function() {
                elem.trigger('liszt:updated');
            });
            scope.$watch(attrs['ngModel'], function() {
                elem.trigger('liszt:updated');
            });
            elem.chosen({ width: attrs['width']});

        }
    };
});