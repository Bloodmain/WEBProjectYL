const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]');

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

$('.comment-input').focusin(function () {
    $(this).toggleClass('focused', true);
})

$('.comment-input').focusout(function () {
    setTimeout(() => {
        $(this).toggleClass('focused', false);
    }, 100);
})

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    var host = document.location.host;
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    return (url === origin || url.slice(0, origin.length + 1) === origin + '/') ||
        (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') ||
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (csrftoken && !csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken.value);
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
                success: function () {
                    likes_counter.text(parseInt(likes_counter.text()) - 1);
                }
            });
        } else {
            $.post('/api/likes', {user: user_id, post: news_id}, function (data) {
                likes_counter.text(parseInt(likes_counter.text()) + 1);
            })
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

$('.send-comment').click(function () {
    var post_id = $(this).attr('class').split(' ')[3];
    $.get('/api/user', {}, function (data) {
        if ('Error' in data)
            return;

        var user_id = data['user']['user'];
        $('.comment-input').each(function (index, el) {
            var id = el.classList[2];
            if (id === post_id) {
                var text = el.value;
                $.post('/api/comments', {user: user_id, post: post_id, text: text}, function () {
                    remember_offset(post_id);
                    location.reload()
                })
                el.value = '';
                return;
            }
        })
    })
})

function remember_offset(post_id) {
    $('.news').each(function (index, el) {
        var id = el.classList[1];
        if (id === post_id) {
            document.cookie = 'reload_offset=' + el.offsetTop
            return
        }
    })
}

function get_cookie(cookie_name) {
    var results = document.cookie.match('(^|;) ?' + cookie_name + '=([^;]*)(;|$)');

    if (results)
        return (unescape(results[2]));
    else
        return null;
}

function delete_cookie(cookie_name) {
    var cookie_date = new Date();
    cookie_date.setTime(cookie_date.getTime() - 1);
    document.cookie = cookie_name += "=; expires=" + cookie_date.toGMTString();
}

$(function () {
    var cookie = get_cookie('reload_offset')
    $('.cont').animate({scrollTop: cookie}, 0);
    delete_cookie('reload_offset')
})

$('.delete-news').click(function () {
    if (confirm('Вы действительно хотите удалить эту запись?')) {
        var element = $(this)
        var news_id = element.attr('class').split(' ')[1];
        $.ajax({
            type: 'DELETE',
            url: '/api/news/' + news_id,
            data: {},
            dataType: 'json',
            success: function () {
                var post_id = element.attr('class').split(' ')[2];
                remember_offset(post_id);
                location.reload()
            }
        });
    }
})

$('.delete-repost').click(function () {
    if (confirm('Вы действительно хотите удалить этот репост?')) {
        var element = $(this)
        var repost_id = element.attr('class').split(' ')[1];
        $.ajax({
            type: 'DELETE',
            url: '/api/reposts/' + repost_id,
            data: {},
            dataType: 'json',
            success: function () {
                var post_id = element.attr('class').split(' ')[2];
                remember_offset(post_id);
                location.reload()
            }
        });
    }
})

$('.delete-comment').click(function () {
    if (confirm('Вы действительно хотите удалить этот комментарий?')) {
        var element = $(this)
        var comment_id = element.attr('class').split(' ')[1];
        $.ajax({
            type: 'DELETE',
            url: '/api/comments/' + comment_id,
            data: {},
            dataType: 'json',
            success: function () {
                var post_id = element.attr('class').split(' ')[2];
                remember_offset(post_id);
                location.reload();
            }
        });
    }
})

$('.repost-img').click(function () {
    if (confirm('Вы действительно хотите создать репост этой записи?')) {
        var element = $(this);
        var post_id = element.attr('class').split(' ')[1];
        $.get('/api/user', {}, function (data) {
            if ('Error' in data)
                return;

            var user_id = data['user']['user'];
            $.post('/api/reposts', {user: user_id, posts: post_id}, function () {
                remember_offset(post_id);
                location.reload();
            })
        })
    }
})

$('.send-friend-request').click(function () {
    var element = $(this);
    var requester_id = element.attr('class').split(' ')[1];
    var friend_id = element.attr('class').split(' ')[2];
    $.post('/api/friends_requests', {requester: requester_id, friend: friend_id}, function () {
        location.reload();
    })
})

$('.delete-from-friends').click(function () {
    var element = $(this);
    var user1_id = element.attr('class').split(' ')[1];
    var user2_id = element.attr('class').split(' ')[2];
    $.ajax({
        type: 'DELETE',
        url: '/api/friends/' + user1_id + '/' + user2_id,
        data: {},
        dataType: 'json',
        success: function () {
            location.reload();
        }
    });
})

$('.remove-friend-request').click(function () {
    var element = $(this);
    var user1_id = element.attr('class').split(' ')[1];
    var user2_id = element.attr('class').split(' ')[2];
    $.ajax({
        type: 'DELETE',
        url: '/api/friends_requests/' + user1_id + '/' + user2_id,
        data: {},
        dataType: 'json',
        success: function () {
            location.reload();
        }
    });
})

$('.add-to-friends').click(function () {
    var element = $(this);
    var friend_id = element.attr('class').split(' ')[1];
    var creator_id = element.attr('class').split(' ')[2];
    $.post('/api/friends', {creator: creator_id, friend: friend_id}, function () {
        location.reload();
    })
})

$('.leave-in-subs').click(function () {
    var element = $(this);
    var author = element.attr('class').split(' ')[1];
    var subscriber = element.attr('class').split(' ')[2];
    $.post('/api/subscriber', {author: author, subscriber: subscriber}, function () {
        location.reload();
    })
})

$('.leave-from-subs').click(function () {
    var element = $(this);
    var user1_id = element.attr('class').split(' ')[1];
    var user2_id = element.attr('class').split(' ')[2];
    $.ajax({
        type: 'DELETE',
        url: '/api/subscriber/' + user1_id + '/' + user2_id,
        data: {},
        dataType: 'json',
        success: function () {
            location.reload();
        }
    });
})
