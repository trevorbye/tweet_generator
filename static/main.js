$(function() {
    $("#create-tweet").on("click", function(e) {
        e.preventDefault();
        $("#loading").show();
        var subject = $('#select-box option:selected').text();

        $.ajax({
            "url" : "/get-tweet?subject=" + subject,
            "type" : "GET",
            error: function() {
            },
            success: function(response) {
                $("#loading").hide();
                $("#output-text").text(response)
            }
        });
    });
});