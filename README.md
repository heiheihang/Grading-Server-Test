# Grading-Server-Test

## Install

```
python3 -m pip install django-rq

# on a different thread (console)
py manage.py rqworker default
```

## Testing 

```
cd grading_server

# Nuke the database
rm db.sqlite3
rm -r media/*

# make migrations
python3 manage.py makemigrations
python3 manage.py migrate

# load data
unzip ../data.zip
python3 manage.py loaddata ../fixture.json

# and we should be good
python3 manage.py runserver
```