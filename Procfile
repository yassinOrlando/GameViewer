web: gunicorn myweb.main:app --log-file=-
heroku buildpacks:clear
heroku buildpacks:add --index heroku/python
heroku ps:scale web=1
heroku config:set FLASK_APP=myweb
heroku ps