# App to Planning diet

## About app:
App help to user organize diet, list all days with recipes and details how to make every dinner.

## Requirements
-browser
-Python 3
-Django
-psycopg2 or psycopg2
-psql or other database manager


## How to start?
1. copy files to disc
2. install requirements
3. set settings
4. configure database
5. type in terminal python manage.py runserver

## App description
Ms Maria Iksińska wrote a cookbook that became a bestseller on the cookbook market in Poland and asked us to prepare a meal planning application for her readers. The book of Mrs. Iksińska promotes healthy eating and emphasizes the importance of planning meals in it. She wants to start running workshops across the country where she will teach participants how to plan meals.
Ms. Maria wants to develop her business, and to achieve her goals, she needs a website-business card and a simple meal planning application.

## Plan

* scrumlab – catalog with Django files
  - settings.py – project settings,
  - urls.py – URL's data,
  - local_settings.py.example – local settings, for details check Configure project,
* jedzonko – Django's app catalog.
* static – Catalog with static files; for details Configure project

## Configure project


Remember: don't keep sensitive data under Git's control! Such sensitive data
are, among others data to connect to the database. We keep this data in the file local_settings.py,
which you will not find in this repository (the file is added to . gitignore)!

Take a look at the settings.py file, you will find the following section:

python
try:
    from scrumlab.local_settings import DATABASES
except ModuleNotFoundError:
    print("Brak konfiguracji bazy danych w pliku local_settings.py!")
    print("Uzupełnij dane i spróbuj ponownie!")
    exit(0)


This means that Django will try to import each time it starts up
constant DATABASES from local_settings.py. Keep the data there for connection.
Don't put this file under Git control. To make your work easier, you must prepare
local_settings.py. file should contain
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<databse name>',
        'HOST': 'localhost',
        'PASSWORD': '<databse name>',
        'USER': '<username>',
        'PORT': 5432
    }
}

---

If all is configured right you should see app at your host adres.
