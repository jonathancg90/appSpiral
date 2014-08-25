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
                    angular.element('#step3').removeClass ('active');
                    angular.element('#step4').removeClass ('active');
                }
                if(projectService.step == 2){
                    angular.element('#step1').addClass('active');
                    angular.element('#step2').addClass('active');
                    angular.element('#step3').removeClass ('active');
                    angular.element('#step4').removeClass ('active');
                }
                if(projectService.step == 3){
                    angular.element('#step1').addClass('active');
                    angular.element('#step2').addClass('active');
                    angular.element('#step3').addClass('active');
                    angular.element('#step4').removeClass('active');
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

projectApp.directive('projectActionSteps', function(projectService, $rootScope) {
    return {
        restrict: 'E',
        template: "<div class=\"row-fluid wizard-actions\">\n    <button class=\"btn btn-info btn-save\" ng-click=\"save()\">\n        <i class=\"icon-ok bigger-150\"></i>\n        Grabar\n    </button>\n    <button class=\"btn btn-prev\" ng-click=\"prev()\" ng-show=\"step>1\">\n        <i class=\"icon-arrow-left\"></i>\n        Prev\n    </button>\n\n    <button class=\"btn btn-success btn-next\" data-last=\"Finish \" ng-click=\"next()\" ng-show=\"step<4\">\n        Next\n        <i class=\"icon-arrow-right icon-on-right\"></i>\n    </button>\n</div>",
        priority: 1,
        replace: true,
        link: function(scope, elm, attrs) {
            scope.statusLine = false;
            scope.step = projectService.step;
            scope.project_code = undefined;
            scope.permissions = [];
            scope.position = 0;

            scope.$watch('projectService.project_code', function(newValue) {
                if (newValue) {
                    scope.project_code = newValue;
                }
            });

            scope.$on('setLine', function(event, args) {
                scope.statusLine = true;
            });
            scope.next = function() {
                if(projectService.step <4) {
                    if (scope.statusLine) {
                        if(scope.permissions[scope.position +1] != undefined){
                            scope.position += 1;
                            projectService.step = scope.permissions[scope.position];
                            scope.step = projectService.step;
                        }

                    }
                     else {
                        scope.$emit("setMessage", {
                            'type':  'warning',
                            'message': 'Debe escoger un tipo de proyecto antes de continuar'
                        });
                        $('html, body').animate({
                                scrollTop: '0px'
                            },
                            1000);
                    }
                }
            };
            scope.prev = function() {
                if(projectService.step > 1){
                    if( scope.statusLine) {
                        if(scope.permissions[scope.position -1] != undefined) {
                            scope.position -= 1;
                            projectService.step = scope.permissions[scope.position];
                            scope.step = projectService.step;
                        }
                    }
                }
            };

            scope.$on('setPermissions', function(event, args) {
                scope.permissions = args.permissions;
                if(args.create){
                    if(scope.permissions[0] == 1){
                        //Si tiene permiso
                    } else {
                        // No puede crear proyectos
                    }
                } else {
                    projectService.step = scope.permissions[0];
                    scope.step = projectService.step;
                }

            });
            scope.save =  function() {
                scope.$emit('saveProject', { });
            }
        }
    }
});