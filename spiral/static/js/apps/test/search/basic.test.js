'use strict';

describe('SearchBasicController', function() {
    var scope;

    beforeEach(angular.mock.module('searchApp'));

    beforeEach(angular.mock.inject(function($rootScope, $controller){
        var searchUrls = {
            'basic': '/test',
            'advance': '/test'
        };
        //create an empty scope
        scope = $rootScope.$new();
        //declare the controller and inject our empty scope
        $controller('SearchBasicController', {$scope: scope});
    }));

    it('should have variable text = "Hello World!"', function(){
        expect(scope.prueba).toBe('Hola');
    });

});