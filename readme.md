```Для работы проекта в терминале перейдите в директорию WebProjectYL, где лежит файл manage.py, и запустите команду python manage.py runserver. Перед использованием установить redis-server из папки Доп. ПО (там приложена последняя версия для Windows версию для MAC и Linux можно без труда найти в интернете) и все библиотеки. ВАЖНО redis-server - должен быть установлен на порт 6379 (он стоит по умолчанию)```

Наш проект это социальная сеть "D&K" на Django. Сейчас немного расскажем о её возможностях:
- Зарегистрируйте новый аккаунт или воспользуйтесь уже существующим (логины и пароли для них будут в конце файла). Реализовано с помощью моделей и форм для из наполнения. Есть API для представления.
- Вы можете оставлять записи прикладывая любое количество файлов. Реализовано с помощью моделей и форм. Есть API для представления.
- Сделать репост любой записи себе на стену. Так же есть возможность перейти к оригинальной записи и просмотр одной записи в целом. Реализовано с помощью моделей и форм. Есть API для представления.
- Вы можете лайкать или комментировать записи и репосты. Реализовано с помощью моделей и API + JS. Вкратце JS-код отправляет со страницы API запрос)))
- Добавлять, удалять друзей. Отправлять запросы в друзья. Есть несколько состояний между 2 пользователями. 
    1. User1 отправил запрос в друзья User2
    2. User1 подписан на User2
    3. User1 в друзьях у User2 (работает в обе стороны)
    4. User2 отправил запрос в друзья User1
    5. User2 подписан на User1
    6. User1 и User2 не связаны
    
- Переписка с другими пользователями в режиме реального времени с помощью моделей и библиотеки channels.
- Сообщества. Вы можете создать сообщество или стать участником какого-нибудь другого. Будучи создателем вы можете назначать админов, которые могут публиковать и удалять записи. Вы так же можете это делать.

Весь код html сделан из шаблонов.
В целом все возможности описаны выше. В код есть небольшие комментарии по моделям и API. Удачного конкурса :smiley:.

Данные для уже созданных пользователей.
  1. Логин: Admin. Пароль Admin12345 (аккаунт суперюзера1)
  2. Логин: User1. Пароль: User12345.
  3. Логин: User2. Пароль: User12345.
  4. Логин: User3. Пароль: user12345.
  5. Логин: User4. Пароль: user12345.