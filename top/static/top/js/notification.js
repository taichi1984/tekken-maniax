$(document).ready(function () {
    initialize_event_handler();
});

function initialize_event_handler() {
    already_read_notification();
    already_read_notification_all()
}

/*ここから、ajaxをdjangoで使うためのおまじない（csrf_token) */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

/*ここまで、ajaxをdjangoで使うためのおまじない（csrf_token) */

function already_read_notification() {
    $(document).on('click', 'input[name="alreadyRead"]', function () {
        $.ajax(
            {
                url: "/notification_check/",
                type: 'POST',
                dataType: 'html',
                data: {
                    notification_id: this.id, url: location.href
                },
                timeout: 3000,
            }).done(function (data) {

        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            alert(data);
        })


    });
}

function already_read_notification_all(){
        $(document).on('click', 'input[name="alreadyReadAll"]', function () {
        $.ajax(
            {
                url: "/notification_check_all/",
                type: 'POST',
                dataType: 'html',
                data: {

                },
                timeout: 3000,
            }).done(function (data) {
                $("input[name=alreadyRead]").prop('checked',true);

        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            alert(data);
        })


    });

}