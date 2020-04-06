$(document).ready(function () {
    initialize_event_handler();

});

function initialize_event_handler() {
    add_good_evaluation();
    add_bad_evaluation();
    delete_good_evaluation()
    delete_bad_evaluation()
    add_favorite();
    release_favorite();
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

function add_good_evaluation() {
    $(document).on('click', 'button[name="good_evaluation"]', function () {

        $.ajax(
            {
                url: "/guide/vote_evaluation/",
                type: 'POST',
                dataType: 'html',
                data: {vote: "1", url: location.href},
                timeout: 3000,
                success: function (data) {
                    info = JSON.parse(data)
                    $('#good_evaluation_area').html(info[0] + ":" + info[1]);
                    $('#bad_evaluation_area').html('<button type="button" class="bad_evaluation_button" name="bad_evaluation"value="bad_evaliation">' +
                        '<img src="/static/guide/image/bad_evaluation.jpg" width="20px"></button> ' + info[2])


                },
                error: function (data) {
                    alert(data);
                }
            })
    });
}

function add_bad_evaluation() {
    $(document).on('click', 'button[name="bad_evaluation"]', function () {

        $.ajax(
            {
                url: "/guide/vote_evaluation/",
                type: 'POST',
                dataType: 'html',
                data: {
                    vote: "2", url: location.href
                },
                timeout: 3000,
            }).done(function (data) {
            info = JSON.parse(data);
            $('#bad_evaluation_area').html(info[0] + ":" + info[2]);
            $('#good_evaluation_area').html('<button type="button" class="good_evaluation_button" name="good_evaluation"value="good_evaluation">\n' +
                '<img src="/static/guide/image/good_evaluation.jpg" width="20px"></button>: ' + info[1])
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            alert(data);
        })


    });
}


function delete_good_evaluation() {
    $(document).on('click', 'button[name="good_evaluation_pushed"]', function () {

        $.ajax(
            {
                url: "/guide/vote_evaluation/",
                type: 'POST',
                dataType: 'html',
                data: {vote: "3", url: location.href},
                timeout: 3000,
                success: function (data) {
                    info = JSON.parse(data);
                    $('#good_evaluation_area').html(info[0] + ":" + info[1]);
                },
                error: function (data) {
                    alert(data);
                }
            })
    });
}

function delete_bad_evaluation() {
    $(document).on('click', 'button[name="bad_evaluation_pushed"]', function () {

        $.ajax(
            {
                url: "/guide/vote_evaluation/",
                type: 'POST',
                dataType: 'html',
                data: {vote: "4", url: location.href},
                timeout: 3000,
                success: function (data) {
                    info = JSON.parse(data);
                    $('#bad_evaluation_area').html(info[0] + ":" + info[2]);
                },
                error: function (data) {
                    alert(data);
                }
            })
    });
}

function add_favorite() {
    $(document).on('click', 'button[name="add_favorite"]', function () {

        $.ajax(
            {
                url: "/guide/add_favorite/",
                type: 'POST',
                dataType: 'html',
                data: {favorite: "1", url: location.href},
                timeout: 3000,
                success: function (data) {
                    $('#page_summary_favorite').html(data)
                },
                error: function (data) {
                    alert(data);
                }
            })
    });
}

function release_favorite() {
    $(document).on('click', 'button[name="release_favorite"]', function () {

        $.ajax(
            {
                url: "/guide/add_favorite/",
                type: 'POST',
                dataType: 'html',
                data: {favorite: "0", url: location.href},
                timeout: 3000,
                success: function (data) {
                    $('#page_summary_favorite').html(data)
                },
                error: function (data) {
                    alert('error');
                }
            })
    });
}