angular.module('searchApp').filter('textFilter', function($rootScope) {
    function omitirAcentos(text) {
        var acentos = "ÃÀÁÄÂÈÉËÊÌÍÏÎÒÓÖÔÙÚÜÛãàáäâèéëêìíïîòóöôùúüûÑñÇç";
        var original = "AAAAAEEEEIIIIOOOOUUUUaaaaaeeeeiiiioooouuuunncc";
        for (var i=0; i<acentos.length; i++) {
            text = text.replace(acentos.charAt(i), original.charAt(i));
        }
        return text;
    }

    return function (items, frase) {
        if (frase != undefined && items != undefined) {
            var arrayToReturn = [];
            frase = frase.substr($rootScope.countInitial.length,  frase.length);
            if(frase.length == 0)
                return items;
            console.log(frase);
            //Recorre cada uno de los resultados del search
            for (var i=0; i<items.length; i++) {
                var validate = false;
                var words = items[i].name_complete.toUpperCase().split(" ");
                //Recorre cada uno e las palabras del campo
                for (var x=0; x<words.length; x++){
                    var palabras = frase.toUpperCase().split(" ");
                    //Recorre cada uno e las palabras escritas en el input
                    for (var y=0; y<palabras.length; y++){
                        if(palabras[y] == "" || palabras[y] == "")
                            continue;

                        words[x] = omitirAcentos(words[x]);
                        palabras[y] = omitirAcentos(palabras[y]);

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