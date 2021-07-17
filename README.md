# Django Selenium Docker

Here is a webapp that displays the Selenium window preview in a Django Admin.

![Selenium Docker preview](https://static.snoweb.fr/media/selenium-docker-github-readme.gif)

In this simple example, we display the urls of the following pages:

- https://www.facebook.com/
- https://www.linkedin.com/
- https://www.instagram.com/
- https://twitter.com/

This minimalist webapp was designed to help you configure the Python ecosystem with Selenium.

The webapp uses the following services :

- [Selenium](https://github.com/SeleniumHQ/selenium)
- [Docker](https://www.docker.com/)
- [Django](https://github.com/django/django) (Webapp)
- [Postgresql](https://www.postgresql.org/) (Database)
- [Celery](https://github.com/celery/celery) (Task)
- [RabbitMQ](https://www.rabbitmq.com/) (Broker)
- [Django channels](https://github.com/django/channels) (Websocket)
- [Redis](https://redis.io/) (Channel layers)

## Run the webapp

### Run with Docker

1 - Check and stop all the following services if they are running on your local machine :

    service rabbitmq-server stop
    service postgresql stop
    service redis-server stop

2 - And run :

    docker-compose up
    docker-compose exec -T app python manage.py on_start --settings=settings.production

3 - Login with django:selenium at :

    http://127.0.0.1:8001/

### Or run locally

1 - You need to run/install these services :

    sudo service rabbitmq-server start
    sudo service redis-server start
    sudo service postgresql start

2 - Then configure your database by following the Django settings.dev configuration :

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'app',
            'USER': 'app_user',
            'PASSWORD': 'changeme',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

3 - Then launch the webapp and the worker :

    export DJANGO_SETTINGS_MODULE=settings.dev
    pip install -r requirements.txt
    python manage.py on_start --settings=settings.dev
    python manage.py runserver 127.0.0.1:4243 -v 3 --settings=settings.dev
    celery -A app.core worker -l info

4 - Login with django:selenium at :

    http://127.0.0.1:4243/
