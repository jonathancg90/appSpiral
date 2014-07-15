//@ Padre afecta al hijo
//& hijo afecta al padre
//= ambos a la vez

projectApp.directive('projectSteps', function(projectService) {
    return {
        restrict: 'E',
        template: "            <div id=\"fuelux-wizard\" class=\"row-fluid hide\" data-target=\"#step-container\">\n                <ul class=\"wizard-steps\">\n                    <li id=\"step1\" data-target=\"#step1\">\n                        <span class=\"step\">1</span>\n                        <span class=\"title\">Datos del proyecto</span>\n                    </li>\n\n                    <li id=\"step2\" data-target=\"#step2\">\n                        <span class=\"step\">2</span>\n                        <span class=\"title\">Detalles de modelos</span>\n                    </li>\n\n                    <li id=\"step3\" data-target=\"#step3\">\n                        <span class=\"step\">3</span>\n                        <span class=\"title\">Informacion de pagos</span>\n                    </li>\n\n                    <li id=\"step4\" data-target=\"#step4\">\n                        <span class=\"step\">4</span>\n                        <span class=\"title\">Recursos</span>\n                    </li>\n                </ul>\n            </div>\n",
        priority: 1,
        replace: true,
        link: function(scope, elm, attrs) {
            scope.statusline = false;

            scope.$watch(function() {
                updateStep();
             });

            function updateStep(){
                if(projectService.step == 1){
                    angular.element('#step1').addClass('active');
                    angular.element('#step2').removeClass ('active');
                }
                if(projectService.step == 2){
                    angular.element('#step1').addClass('active');
                    angular.element('#step2').addClass('active');
                    angular.element('#step3').removeClass ('active');
                }
                if(projectService.step == 3){
                    angular.element('#step1').addClass('active');
                    angular.element('#step2').addClass('active');
                    angular.element('#step3').addClass('active');
                    angular.element('#step4').removeClass ('active');
                }
                if(projectService.step == 4){
                    angular.element('#step1').addClass('active');
                    angular.element('#step2').addClass('active');
                    angular.element('#step3').addClass('active');
                    angular.element('#step4').addClass('active');
                }
            }
        }
    }
});

projectApp.directive('projectActionSteps', function(projectService) {
    return {
        restrict: 'E',
        template: "<div class=\"row-fluid wizard-actions\">\n    <button class=\"btn btn-prev\" ng-click=\"prev()\">\n        <i class=\"icon-arrow-left\"></i>\n        Prev\n    </button>\n\n    <button class=\"btn btn-success btn-next\" data-last=\"Finish \" ng-click=\"next()\">\n        Next\n        <i class=\"icon-arrow-right icon-on-right\"></i>\n    </button>\n</div>",
        priority: 1,
        replace: true,
        link: function(scope, elm, attrs) {
            scope.statusLine = false;

            scope.$on('setLine', function(event, args) {
                scope.statusLine = true;
            });
            scope.next = function() {
                if(projectService.step <4){
                    if( scope.statusLine) {
                        projectService.step += 1;
                    } else {
                        scope.$emit("setMessage", {
                            'type':  'warning',
                            'message': 'Debe escoger un tipo de proyecto antes de continuar'
                        });
                    }
                }
            };
            scope.prev = function() {
                if(projectService.step > 1){
                    if( scope.statusLine) {
                        projectService.step -= 1;
                    }
                }
            };
        }
    }
});