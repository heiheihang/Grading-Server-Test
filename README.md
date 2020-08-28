# Grading-Server-Test

##Run
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

#on a different thread 
redis-server

# on a different thread (console)
python manage.py rqworker default
```

## Install

```
pip install django
pip install django-bootstrap-form
python -m pip install django-rq
```

## Testing 

```
cd grading_server

# Nuke the database
rm db.sqlite3
rm -r media/*

# make migrations
python manage.py makemigrations
python manage.py migrate

# load data
unzip ../data.zip
python manage.py loaddata ../fixture.json

# and we should be good
python manage.py runserver
```
