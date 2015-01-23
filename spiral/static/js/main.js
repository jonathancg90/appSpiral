$(document).on('ready', function(){

    $('#modalSupportOpen').on('click', function(){
        $('.message-support').hide();

    });

    $('#registerSupport').on('click', function(){
        var url = $('#formSaveSupport').attr('action'),
            data = {
                'text': $('#supportText').val()
            };


        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: function(data){
                if(data.status == 'success'){
                    $('#supportText').val('');
                    $('#modalSupportSucess').show()
                } else {
                    $('#modalSupportWarning').show()
                }
            },
            error: function(data){
                $('#modalSupportError').show();
            },
            dataType: 'json'
        });
    });
});