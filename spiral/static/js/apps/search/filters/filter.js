angular.module('AdvanceFilter',[]).filter('criterios', function(){
    return function(items, texto){
        var arrayToReturn = [],
            maximo=0;
        for (var i=0; i<items.length; i++){
            if(texto == undefined){
                arrayToReturn.push(items[i]);
            } else{
                //obtener cantidad de palabras en el texto (puntaje maximo)
                //una palabra comparo con todos los campos(si hay uno == suma +1 )
                //si el puntaje es = a la cantida dde encontrados == push

                var palabras = texto.split(" ");
                if(palabras.length >1){
                    var puntaje = 0;
                    for (var ind=0; ind<palabras.length; ind++){
                        if(palabras[ind] == items[i].carracteristicas.genero){
                            puntaje++;
                        }
                        if(palabras[ind] == items[i].carracteristicas.profesion){
                            puntaje++;
                        }
                        if(palabras[ind] == items[i].carracteristicas.cabello){
                            puntaje++;
                        }
                        if(palabras[ind] == items[i].carracteristicas.estatura){
                            puntaje++;
                        }
                    }
                    items[i].carracteristicas.puntaje = puntaje;
                    if(puntaje>maximo){
                        maximo=puntaje;
                    }

                } else {
                    arrayToReturn.push(items[i]);
                }
            }
        }
        if(maximo > 0){
            for (var i=0; i<items.length; i++){
                if(items[i].carracteristicas.puntaje == maximo){
                    arrayToReturn.push(items[i]);
                }
            }
        }

        return arrayToReturn;
    };
});
