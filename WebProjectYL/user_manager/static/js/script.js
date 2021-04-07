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

$('.like_img').click(function () {
    $(this).toggleClass('liked')
})