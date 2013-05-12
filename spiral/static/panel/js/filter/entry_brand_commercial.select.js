$(function(){
    var entry = $('.form-entry');
    var brand = $('.form-brand');
    var commercial = $('.form-commercial');

    if(entry.length > 0) {
        console.log('1');
        entry.change(setBrand);
        entry.addClass('chzn-select');
        entry.chosen({});
    }
    if(brand.length > 0) {
        brand.change(setCommercial);
        brand.addClass('chzn-select');
        brand.chosen({});
    }
    if(commercial.length > 0) {
        commercial.addClass('chzn-select');
        commercial.chosen({});
    }

    function setBrand(){

        var value = $(this).find('option:selected').val();
        var url = url_brand_by_entry;
        //Selecciono opcion valida
        if (value !== undefined && value.length !== 0) {
            url=url.replace("0",value);
        } else {
            brand.empty();
            brand.trigger("liszt:updated");
            if(commercial.length > 0) {
                commercial.empty();
                commercial.trigger("liszt:updated");
            }
        return;
        }

        $.ajax({
             url: url,
             dataType:'json',
             success : function(data){
                 brand.trigger("liszt:updated");
                 brand.empty();
                 brand.append("<option value=''>--------------</option>");
                 if(commercial.length > 0) {
                    commercial.empty();
                 }

             $.each(data['brand'],function(i, value){
                brand.append("<option value="+value['id']+">"+value['name']+"</option>");
             });
         },
         complete : function(){
             //Actualizacion e inicializacion de chosen
             brand.trigger("liszt:updated");
             if(commercial.length > 0) {
                commercial.trigger("liszt:updated");
             }
             brand.chosen();
             }
         });
    }

    function setCommercial() {

    }
/*
    //Asignar clase de chozen
    country.addClass('chzn-select');
    country.chosen();
    state.addClass('chzn-select');
    city.addClass('chzn-select');
    //Validacion despues de haber realziado una busqueda
    console.log('a: '+state.find('option:selected').val())
    if(country.find('option:selected').val().length !== 0 ){
        state.chosen();
    }
    if(state.find('option:selected').val().length !== 0 ){
        state.chosen();
        city.chosen();
    }
    if(city.find('option:selected').val().length !== 0 ){
        city.chosen();
    }
    //Cargar estados de los paises
    function setStates(){
        var value = $(this).find('option:selected').val();
        var url = url_states_by_country;
        //Selecciono opcion valida
        if (value !== undefined && value.length !== 0) {
            url=url.replace("0",value);
        } else {
            state.empty();
            city.empty();
            state.trigger("liszt:updated");
            city.trigger("liszt:updated");
            return;
        }
        $.ajax({
                url: url,
                dataType:'json',
                success : function(data){
                    state.trigger("liszt:updated");
                    state.empty();
                    state.append("<option value=''>--------------</option>");
                    city.empty();

                $.each(data['result'],function(i, value){
                state.append("<option value="+value[0]+">"+value[1]+"</option>");
                });
            },
            complete : function(){
                //Actualizacion e inicializacion de chosen
                state.trigger("liszt:updated");
                city.trigger("liszt:updated");
                state.chosen();
                }
            });

    };
    //Cargar las ciudades de el estado seleccionado
    function setCity(){
        console.log("ciudad: "+city);
        city.trigger("liszt:updated");
        var value = $(this).find('option:selected').val();
        var url = url_city_by_states;
        //Selecciono opcion valida
        if (value !== undefined) {
            url=url.replace("0",value);
        }
        $.ajax({
            url : url,
            dataType : 'json',
            success : function(data){
                city.empty();
                city.append("<option value=''></option>");
                $.each(data['cities'],function(i, value){
                    city.append("<option value="+value['id']+">"+value['name']+"</option>");
                });
        },
        complete : function(){
            //Actualizacion e inicializacion de chosen
            city.trigger("liszt:updated");
            city.chosen();
            }
        });
    }*/
});
