const chatID = JSON.parse(document.getElementById('chat-id').textContent);
const user = JSON.parse(document.getElementById('user').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + chatID
    + '/'
);

var first_message = true;

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (first_message) {
        first_message = false;
        for (var k in data.messages) {
            var message = data.messages[k];
            var tp = 'other-message'
            if (message[1] === user) {
                tp = 'our-message'
            }
            $('.table-chat tr:last').after('<tr><td class="' + tp + '"><div class="date-send">' + message[2] + '</div><br><div class="message">' + message[0] + '</div></td></tr>');
        }
    } else {
        var tp = 'other-message'
        if (data.uid === user) {
            tp = 'our-message'
        }
        if (!data.message) {
            return;
        }
        $('.table-chat tr:last').after('<tr><td class="' + tp + '"><div class="date-send">' + data.date + '</div><br><div class="message">' + data.message + '</div></td></tr>');
    }
    var div = $(".dialog");
    div.scrollTop(div.prop('scrollHeight'));
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};


$('.message-input').focus();
$('.message-input').keyup(function (e) {
    if (e.keyCode === 13) {
        $('.send-message').click();
    }
})

$('.send-message').click(function () {
    const inputDOM = $('.message-input')
    chatSocket.send(JSON.stringify({
        'message': inputDOM.val()
    }));
    inputDOM.val('');
})