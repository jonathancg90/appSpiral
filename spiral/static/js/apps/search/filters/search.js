angular.module('searchApp').filter('textFilter', function($rootScope) {
    return function (items, frase) {
        if (frase != undefined && items != undefined) {
            var arrayToReturn = [];
            frase = frase.substr($rootScope.countInitial.length,  frase.length);
            if(frase.length == 0)
                return items;
            console.log(frase);
            for (var i=0; i<items.length; i++) {
                var validate = false;
                var words = items[i].name_complete.toUpperCase().split(" ");
                console.log('Nombre: '+items[i].name_complete);
                for (var x=0; x<words.length; x++){
                    var palabras = frase.toUpperCase().split(" ");
                    console.log(palabras);
                    for (var y=0; y<palabras.length; y++){
                        if(palabras[y] == "" || palabras[y] == "")
                            continue;
                        validate = words[x].indexOf(palabras[y]) != -1?true:false;
                        if(validate){
                            arrayToReturn.push(items[i]);
                            break;
                        }
                    }
                    if(validate){
                        break;
                    }
                }
            }
            return arrayToReturn;
        } else {
            return items;
        }
    }
});