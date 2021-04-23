heroku config:set DISABLE_COLLECTSTATIC=1
web: gunicorn WebProjectYL.wsgi --log-file -
web: python WebProjectYL\manage.py runserver
