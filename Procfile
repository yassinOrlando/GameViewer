web: gunicorn myweb.main:app --log-file=-
heroku ps:scale web=1
heroku config:set FLASK_APP=myweb
heroku ps