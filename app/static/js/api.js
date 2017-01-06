$(document).ready(function() {
    $("#search-form").submit(function(e) {
        $.ajax( {
            type: "GET",
            url: $("form#search-form").attr( 'action' ),
            data: $("form#search-form").serialize(),
            success: function( response ) {
                $('#query-result-content').html(response);
                $('#index-page-content').hide();
            },
            error: function (xhr, status) {
                console.log("Sorry, there was a problem!");
            },
            complete: function (xhr, status) {
                $('#query-result-content').slideDown('slow')
            }
            });
        e.preventDefault();
    });
});