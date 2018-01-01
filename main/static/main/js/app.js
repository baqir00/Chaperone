/**
 * Created by baqir on 20-11-2017.
 */

$('#spojbtn').click(function() {
  var username = $('#spoj').val();
    $.ajax({
        url: '/validate_spoj/',
        data: {
          'username': username
        },
        dataType: 'json',
        success: function (d) {
            $('#spojbtna').text(d.data);
        }
      });
});

$('#hackerearthbtn').click(function() {
  var username = $('#hackerearth').val();
    $.ajax({
        url: '/validate_hackerearth/',
        data: {
          'username': username
        },
        dataType: 'json',
        success: function (d) {
            $('#hackerearthbtna').text(d.data);
        }
      });
});

$('#codechefbtn').click(function() {
  var username = $('#codechef').val();
    console.log(username)
    $.ajax({
        url: '/validate_codechef/',
        data: {
          'username': username
        },
        dataType: 'json',
        success: function (d) {
            $('#codechefbtna').text(d.data);
        }
      });
});


$('#compile').click(function() {
    var lang = $("#lang").val();
    var code = $("#code").val();
    $.ajax({
        url: '/validate_compile/',
        data: {
            'lang': lang,
            'code': code
        },
        dataType: "json",
        success: function (d) {
            var status = JSON.parse(JSON.stringify(d)).compile_status;
            if(status=="OK") {
                $("#message").addClass("alert-success").removeClass("alert-danger").removeClass("d-none").text("Success");
            }
            else {
                $("#message").addClass("alert-danger").removeClass("alert-success").removeClass("d-none").text(status);

            }
        }
      });
});


$('#run').click(function() {
    var lang = $("#lang").val();
    var code = $("#code").val();
    var id = parseInt($("#id").text());
    $.ajax({
        url: '/validate_run/',
        data: {
            'lang': lang,
            'code': code,
            'id' : id
        },
        dataType: "json",
        success: function (d) {
            var status = JSON.parse(JSON.stringify(d)).run_status;
            var error = d.error;
            if(!error) {
                $("#message").addClass("alert-success").removeClass("alert-danger").removeClass("d-none").text(status);
            }
            else {
                $("#message").addClass("alert-danger").removeClass("alert-success").removeClass("d-none").text("Compilation Error");
            }
        }
      });
});