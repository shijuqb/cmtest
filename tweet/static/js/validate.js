$(function(){
    /*
        validate - tweet submit form
    */
    $("#tweet_form").validate({
        errorElement: "em",
        errorPlacement: function (error, element) {
            error.appendTo(element.parent().closest('p'));
        },
        rules: {
            content: {
                required: true,
                maxlength: 140
            }
        },
        messages: {
            content: {
                required: "This field is required",
                maxlength: "Maximum limit reached"
            }
        }
    });

    /*
        check characters left on content element keyup
    */
    $('#id_content').keyup(function() {
        textCounter(this,'counter',140)
    });
});   

// counting the characters left
function textCounter(field,field2,maxlimit){
    var countfield = document.getElementById(field2);
    if ( field.value.length > maxlimit ) {
        field.value = field.value.substring( 0, maxlimit );
        return false;
    } else {
        countfield.value = maxlimit - field.value.length;
        //the id of the label showing the updated number of characters remaining
        $('#counter').text(countfield.value);
    }
} 