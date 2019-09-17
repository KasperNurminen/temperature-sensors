# Temperature sensors

This application collects and aggregates data from a dummy SQLlite-file and displays them in index.html. Backend is implemented with Django, and is deployed with Docker and gunicorn.

# How to run it:
The easy way (in backend-directory):
```
docker-compose up -d 
````

The hard way:

Run the following commands in the backend-directory:
````
- pip install -r requirements.txt
- SECRET_KEY=randomstring python manage.py migrate --fake
- SECRET_KEY=randomstring python manage.py runserver 8080
````
You can also of course create an .env-file for the secret key.

Tests can be ran with 
```
SECRET_KEY=randomstring python manage.py test 
````

## Notes on backend implementation
- The supplied SQLite file didn't, as SQLlite files often don't, have any explicit primary keys. Django does not like that, and after a bit of tinkering I conceded that I will simply use timestamps as primary keys. This is _NOT GOOD_ but I also didn't want to do a whole data migration and have Django ORM manage the primary keys. I can expand on this further, but long story short, I didn't find an easy way to implement primary keys any other way.

- Due to the above problems, running the django migrations requires the `--fake` -flag. The database is not being managed by Django, so we can only fake the migrations and not actually do them

- Also due to the above problems, the the test suite actually uses Django-managed database. This is achieved by having `managed': settings.TESTING` in the migration, and the TESTING-variable is true whenever tests are ran.

- The instructions stated that the weather data is on the first span-element of the site. That was not true, and I had to use a class-attribute to fetch it. I do not know whether it changes over time, so I made a placeholder in case it breaks at some time.

- The data is also fetched at max once a minute and otherwise cached for performance.