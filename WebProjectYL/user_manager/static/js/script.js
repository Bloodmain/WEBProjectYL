const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

$(document).ready(function () {
    $('.avatar').bootstrapFileInput('Выбрать аватар');
    $('.news_files').bootstrapFileInput('Прикрепить файлы');
})

$('.burger, .menu_btn').click(function () {
    $('.burger').toggleClass('open');
    $('.menu').toggleClass('menu_active');
});

$('.news_input, .news_creation, .news_files').focusin(function () {
    $('.news_creation').toggleClass('create', true);
    $('.news_input').toggleClass('create-text', true);
    $('.news_files').toggleClass('create-files', true);
    $('.file-input-name').toggleClass('opened', true);
});

$('.news_input').focusout(function () {
    $('.news_creation').toggleClass('create', false);
    $('.news_input').toggleClass('create-text', false);
    $('.news_files').toggleClass('create-files', false);
    $('.file-input-name').toggleClass('opened', false);
});

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    var host = document.location.host;
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.like_img').click(function () {
    var element = $(this);
    element.toggleClass('liked');
    var news_id = element.attr('class').split(' ')[1];
    var likes_counter = $('.likes_counter-' + news_id);
    console.log(likes_counter.text())

    $.get('/api/user', {}, function (data) {
        if ('Error' in data)
            return
        var user_id = data['user']['user'];

        if (!element.hasClass('liked')) {
            $.ajax({
                type: 'DELETE',
                url: '/api/likes/' + user_id + '_' + news_id,
                data: {},
                dataType: 'json',
            });
            likes_counter.text(parseInt(likes_counter.text()) - 1);
        } else {
            $.post('/api/likes', {user: user_id, post: news_id}, function (data) {})
            likes_counter.text(parseInt(likes_counter.text()) + 1);
        }
    })
})

$(document).ready(function () {
    $.get('/api/user', {}, function (data) {
        if ('Error' in data)
            return
        var user_id = data['user']['user'];

        $('.like_img').each(function (index, el) {
            var news_id = el.classList[1];
            var req = user_id + '_' + news_id;
            $.get('/api/likes/' + req, {}, function (data) {
                if (!('Error' in data))
                    $(el).toggleClass('liked', true);
            })
        })
    })
})